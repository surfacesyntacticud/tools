open Printf

let infile = Sys.argv.(1)

let in_ch = open_in infile

let rev_lines = ref []

let _ =
  let rec loop () =
    rev_lines := (input_line in_ch) :: !rev_lines;
    loop () in
  try loop () with End_of_file -> ()

let rev_array = Array.of_list !rev_lines

let _ =
  let skip = ref None in
  for i = (Array.length rev_array - 1) downto 0 do
    match Str.split (Str.regexp "\t") rev_array.(i) with
    | [] -> skip := None
    | [id; _; _; _; _; _; _; _; _; _] -> 
      begin
        match (Str.split (Str.regexp "-") id, !skip) with
        | ([l;r],_) -> skip := Some (int_of_string l, int_of_string r)
        | ([id], Some (l,r)) when l <= (int_of_string id) && (int_of_string id) <= r -> rev_array.(i) <- "*" ^ rev_array.(i)
        | _ -> ()
      end
    | _ -> ()
  done

let _ =
  let text = ref "" in
  Array.iteri 
    (fun i l -> match l with
      | "" -> text := ""
      | l when String.length l > 8 && String.sub l 0 8 = "# text =" -> rev_array.(i) <- "# text = " ^ !text
      | l when l.[0] = '*' -> rev_array.(i) <- String.sub rev_array.(i) 1 ((String.length rev_array.(i)) - 1)
      | l -> 
        match Str.split (Str.regexp "\t") l with
        | [id; form; _; _; _; _; _; _; _; misc] ->
          begin
            let misc_feats = Str.split (Str.regexp "|") misc in
            text:= sprintf "%s%s%s" form (if List.mem "SpaceAfter=No" misc_feats || !text="" then "" else " ") !text;
          end
        | _ -> ()
    ) rev_array;

  for i = (Array.length rev_array) - 1 downto 0 do
    printf "%s\n" rev_array.(i)
  done
