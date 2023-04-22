var urlParams = new URLSearchParams(window.location.search);
var md = new Remarkable();

var app = new Vue({
  el: '#app',
  data: {
    json: {
      display_modes: [],  // need to be initialized for proper html starting
    },
    gridApi: null,
    filter_kind: "rows", // can be "rows" or "cols"
    filter_value: "",
    display_mode: 0,
    title: "",
  },
  watch: {
    display_mode: function () {
      this.update_sorting();
      this.refresh_columns();
      this.gridApi.redrawRows();
    },
    filter_value: function() { this.refresh_columns() },
    filter_kind: function() { this.refresh_columns() }
  },
  methods: {
    set_display_mode (x) {
      this.display_mode = x;
    },
    update_sorting() {
      this.json.columns.forEach(c => {
        c.comparator= (function (v1,v2) {
          let n1 = v1 == undefined ? 0 : v1[app.display_mode];
          let n2 = v2 == undefined ? 0 : v2[app.display_mode];
          return n1 - n2
        });
      });
    },
    // method called both atfer filering changes and display mode change (sorting should be changed)
    refresh_columns(){
      if (app.filter_value == "") {
        this.gridApi.setRowData(this.json.cells) // all rows
        this.gridApi.setColumnDefs([col0,col1].concat(this.json.columns)) // all cols
      } else {
        if (app.filter_kind == "rows") {
          const re = new RegExp(this.filter_value, 'i');
          let filtered_rows = this.json.cells.filter(l => l.row_header.match(re));
          this.gridApi.setRowData(filtered_rows);
          const cols = new Set()
          filtered_rows.forEach((item, i) => {
            var keys = Object.keys(item);
            keys.forEach(cols.add, cols);
          });
          let filtered_cols = this.json.columns.filter(l => cols.has(l.field));
          this.gridApi.setColumnDefs([col0,col1].concat(filtered_cols));
        } else {
          const re = new RegExp(this.filter_value, 'i');
          let filtered_cols = this.json.columns.filter(function (l) { console.log (l); return l.field.match(re)});
          this.gridApi.setColumnDefs([col0,col1].concat(filtered_cols));
          const fields = new Set()
          filtered_cols.forEach((item, i) => {
            fields.add(item.field)
          });
          let filtered_rows = this.json.cells.filter(l => Object.keys(l).some(k => fields.has(k)));
          this.gridApi.setRowData(filtered_rows);
        }
      }
    },

    cell(params) {
      if (params.value != undefined) {

        // column 1 ==> just print the data
        if (params.colDef.field == "row_header") {
          return `<b>${params.value}</b>`;

        // column 2
        } else if (params.colDef.field == "row_total" && params.data.row_total != undefined) {
          // test if the full row is searchable
          if (app.json.grew_match.row != undefined) {
            return `<a class="btn btn-primary btn-sm" onclick='grew_match("row","${params.data.row_header}","")'>${params.data.row_total}</a>`;
          } else {
            return `<a class="btn btn-secondary disabled btn-sm">${params.value}</a>`;
          }

        // row 2
        } else if (params.data.row_type == "TOTAL") {
          // test if full column is searchable
          if (app.json.grew_match.col != undefined) {
            return `<a class="btn btn-primary btn-sm" onclick='grew_match("col", "", "${params.colDef.field}")'>${params.value}</a>`;
          } else {
            return `<a class="btn btn-secondary disabled btn-sm">${params.value}</a>`;
          }

        // regular cell: row > 2 && col > 2
        } else {
          let style = this.json.display_modes[this.display_mode][1]
          if (style=="PERCENT") {
            v = (params.value[this.display_mode]* 100).toFixed(2) + "%"
          } else {
            v = params.value[this.display_mode]
          }
          return (`<a class="btn btn-success btn-sm" onclick='grew_match("cell", "${params.data.row_header}","${params.colDef.grew}")'>${v}</a>`)
        }
      }
    }
  }
})

const col0 = {
  field: "row_header",
  headerName: "",
  sortingOrder: ['asc', 'desc', null],
  pinned: "left",
  lockPinned: true,
}

let col1 = {
  field: "row_total",
  headerName: "", // Value is set in build_data
  sortingOrder: ['asc', 'desc', null],
  pinned: "left",
  lockPinned: true,
}

function build_grid(data) {
  app.json = data;
  app.title = md.render(app.json.title);
  $('#update_ago').html('<time class="timeago" datetime="' + app.json.timestamp + '">update time</time>');
  $('#update_ago > time').timeago(); // make it dynamic

  app.update_sorting(); // ensure that sorting is done on the right component

  col1.headerName = app.json.col_key;

  const gridOptions = {  
    columnDefs: [col0, col1].concat(app.json.columns),
    defaultColDef: {
      width: 150,
      sortable: true,
      sortingOrder: ['desc', 'asc'],
      resizable: true,
      cellRenderer: app.cell,
    },
    pinnedTopRowData: [app.json.columns_total],
  };
  
  const gridDiv = document.querySelector('#main_grid');
  new agGrid.Grid(gridDiv, gridOptions);
  
  gridOptions.api.setRowData(app.json.cells);
  app.gridApi = gridOptions.api;
}

function esc(s) {
  return (encodeURIComponent(s.replace(/["]/g, '\\\"')))
}

function grew_match(kind, row_header, col_header) {
  // kind can be "cell", "row" or "col"
  let request = app.json.grew_match[kind].replace(/__ROW__/g, esc(row_header)).replace(/__COL__/g, esc(col_header));
  console.log(request);
  window.open(request, '_blank');
}

// setup the grid after the page has finished loading
document.addEventListener('DOMContentLoaded', () => {
  $('[data-toggle="tooltip"]').tooltip()
  
  let file = urlParams.get('data');
  if (file != null) {
    fetch(file + '.json')
    .then((response) => response.json())
    .then((data) => {
      build_grid(data);
      let col_filter = urlParams.get('cols');
      if (col_filter != null) {
        app.filter_kind = "cols";
        app.filter_value = col_filter;
      }
      let row_filter = urlParams.get('rows');
      if (row_filter != null) {
        app.filter_kind = "rows";
        app.filter_value = row_filter;
      }
    })
    .catch((_) => {
      error ('Loading error!', `Cannot find file \`${file}.json\`.`)
    });
  } else {
    window.location = "list.html";
  }
});

function error(title, md_msg) {
  swal({  // See https://github.com/t4t5/sweetalert/issues/801
    title: title,
    content: {
      element: "div",
      attributes: { innerHTML: md.render(md_msg) },
    },
    icon: "error",
  })
}