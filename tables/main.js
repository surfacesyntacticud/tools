var global_grew_match = []
var urlParams = new URLSearchParams(window.location.search);
var md = new Remarkable();


var app = new Vue({
  el: '#app',
  data: {
    portal: true,
    title: "",
    alert: "",
    gridApi: null,
    cells: [],
    filter_kind: "rows", // can be "rows" or "cols"
    filter_value: "",
    columns: [],
    display_mode: 0, // 0 -> occurences, 1 -> ratio per sent, 2 -> ration per token

  },
  watch: {
    display_mode: function () {
      this.update_sorting();
      this.refresh_columns();
      this.gridApi.redrawRows();
    },
    filter_value: function() { this.refresh_columns() } 
  },
  methods: {
    update_sorting() {
      this.columns.forEach(c => { 
        c.comparator= (function (v1,v2) {
          let n1 = v1 == undefined ? 0 : v1[app.display_mode];
          let n2 = v2 == undefined ? 0 : v2[app.display_mode];
          return n1 - n2
        });
      });
    },
    // method called both atfer filering changes and display mode change (sorting should be changed)
    refresh_columns(){
      if (app.filter_kind == "rows") {
        let filtered_rows = this.cells.filter(l => l.treebank.indexOf(this.filter_value) >= 0);
        this.gridApi.setRowData(filtered_rows);
        const cols = new Set()
        filtered_rows.forEach((item, i) => {
          var keys = Object.keys(item);
          keys.forEach(cols.add, cols);
        });
        let filtered_cols = this.columns.filter(l => cols.has(l.field));
        this.gridApi.setColumnDefs([col0].concat(filtered_cols));
      } else {
        let filtered_cols = this.columns.filter(l => l.field.indexOf(this.filter_value) >= 0);
        this.gridApi.setColumnDefs([col0].concat(filtered_cols));
        const fields = new Set()
        filtered_cols.forEach((item, i) => {
          fields.add(item.field)
        });
        let filtered_rows = this.cells.filter(l => Object.keys(l).some(k => fields.has(k)));
        this.gridApi.setRowData(filtered_rows);
      }
    },
    cell(data) {
      if (data.colDef.field == "treebank") {
        return `<B>${data.value}</B>`;
      } else {
        let v = "undef"
        if (data.value != undefined) {
          if (this.display_mode == 0) {
            v = data.value[0];
          } else if (this.display_mode == 1) {
            v = data.value[1].toFixed(4)
          } else if (this.display_mode == 2) {
            v = data.value[2].toFixed(6)
          }
          return (`<a class="btn btn-success btn-sm" onclick='grew_match("${data.data.treebank}","${data.colDef.field}")'>${v}</a>`)
        }
      }
    }
  }
})

const col0 = {
  field: "treebank",
  width: 240,
  pinned: "left",
  lockPinned: true,
  cellClass: "lock-pinned"
}

function build_grid(data) {
  app.portal = false;
  app.title = md.render(data.title);
  app.cells = data.cells;
  app.columns = data.columns;
  app.update_sorting(); // ensure that sorting is done on the right component
  global_grew_match = data.grew_match;
  const gridOptions = {
    columnDefs: [col0].concat(app.columns),
    defaultColDef: {
      width: 150,
      sortable: true,
      resizable: true,
      cellRenderer: app.cell,
    },
  };

  const gridDiv = document.querySelector('#myGrid');
  new agGrid.Grid(gridDiv, gridOptions);
  gridOptions.api.setRowData(app.cells);
  app.gridApi = gridOptions.api;
}

function get_before_whitespace(s) {
  index = s.indexOf(' ');
  if (index == -1) {
    return s
  } else {
    return s.slice(0, index)
  }
}

function grew_match(treebank, field) {
  let pattern = global_grew_match[field]["code"];
  let corpus = get_before_whitespace(treebank);
  let get_param = "?corpus=" + corpus;
  get_param += "&pattern=" + encodeURIComponent(pattern);
  if (global_grew_match[field]["key"] != undefined) {
    get_param += "&clustering=" + encodeURIComponent(global_grew_match[field]["key"]);
  }
  window.open('http://universal.grew.fr' + get_param, '_blank');
}

// setup the grid after the page has finished loading
document.addEventListener('DOMContentLoaded', () => {
  let file = urlParams.get('data');
  if (file != null) {
    fetch(file + '.json')
      .then((response) => response.json())
      .then((data) => build_grid(data))
      .catch((error) => {
        app.alert = md.render(`## Cannot find file \`${file}.json\`.`)
      });
  }

  $('#toggle-state').change(function() {
    app.filter_kind = $(this).prop('checked') ? "rows" : "cols";
    app.filter_value = "";
  })
});