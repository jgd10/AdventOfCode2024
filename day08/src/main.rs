use aoc::InputType;
use itertools::Itertools;
use std::cmp;
use std::collections::HashMap;
use std::collections::HashSet;

use aoc::get_input_as_chars;
use aoc::reconstruct_grid;
use aoc::time_function;
use aoc::write_string_to_file;
use aoc::Coord32;

fn parse(input_type: InputType) -> (HashSet<Coord32>, HashMap<String, HashSet<Coord32>>) {
    let mut coordinates: HashSet<Coord32> = HashSet::new();
    let mut antennas: HashMap<String, HashSet<Coord32>> = HashMap::new();
    let characters: Vec<Vec<char>> = match input_type {
        InputType::Input => get_input_as_chars(include_str!("../input.txt")),
        InputType::Example
        | InputType::Example1
        | InputType::Test
        | InputType::Test1
        | InputType::Test2
        | InputType::Test3 => get_input_as_chars(include_str!("../example.txt")),
        InputType::Example2 => get_input_as_chars(include_str!("../example2.txt")),
    };
    for (j, row) in characters.iter().enumerate() {
        for (i, col) in row.iter().enumerate() {
            let coordinate: Coord32 = Coord32 {
                x: i as i32,
                y: j as i32,
            };
            coordinates.insert(coordinate);
            match col {
                '.' => continue,
                _ => {
                    let existing: &mut HashSet<Coord32> =
                        antennas.entry(col.to_string()).or_insert(HashSet::new());
                    existing.insert(coordinate);
                }
            }
        }
    }
    (coordinates, antennas)
}

fn get_antinode_coords(
    coord1: &Coord32,
    coord2: &Coord32,
    allowed: &HashSet<Coord32>,
    include_harmonics: bool,
) -> HashSet<Coord32> {
    let difference_vector: Coord32 = Coord32 {
        x: coord1.x - coord2.x,
        y: coord1.y - coord2.y,
    };
    let mut antinodes: HashSet<Coord32> = HashSet::new();
    let mut furthest_coord: Coord32;
    // go forward
    furthest_coord = Coord32 {
        x: coord1.x + difference_vector.x,
        y: coord1.y + difference_vector.y,
    };
    while allowed.contains(&furthest_coord) {
        antinodes.insert(furthest_coord);
        furthest_coord = Coord32 {
            x: furthest_coord.x + difference_vector.x,
            y: furthest_coord.y + difference_vector.y,
        };
        if !include_harmonics {
            break;
        }
    }
    // go backward
    furthest_coord = Coord32 {
        x: coord2.x - difference_vector.x,
        y: coord2.y - difference_vector.y,
    };
    while allowed.contains(&furthest_coord) {
        antinodes.insert(furthest_coord);
        furthest_coord = Coord32 {
            x: furthest_coord.x - difference_vector.x,
            y: furthest_coord.y - difference_vector.y,
        };
        if !include_harmonics {
            break;
        }
    }
    if include_harmonics {
        antinodes.insert(*coord1);
        antinodes.insert(*coord2);
    }
    return antinodes;
}

fn find_antinodes(include_harmonics: bool) -> HashSet<Coord32> {
    let input_type = InputType::Input;
    let (coordinates, antennas) = parse(input_type);
    let mut antinodes: HashSet<Coord32> = HashSet::new();
    let mut counter = 0;

    for (_, coords) in antennas.clone() {
        for coord_pair in coords.iter().combinations(2) {
            antinodes.extend(get_antinode_coords(
                coord_pair.get(0).unwrap(),
                coord_pair.get(1).unwrap(),
                &coordinates,
                include_harmonics,
            ));
            visualise(
                coordinates.clone(),
                antinodes.clone(),
                antennas.clone(),
                counter,
                input_type,
                include_harmonics,
            );
            counter += 1;
        }
    }
    antinodes
}

fn part1() {
    let antinodes = find_antinodes(false);
    println!("Part 1: {}", antinodes.len());
}

fn part2() {
    let antinodes = find_antinodes(true);
    println!("Part 2: {}", antinodes.len());
}

fn visualise(
    coordinates: HashSet<Coord32>,
    antinodes: HashSet<Coord32>,
    antennas: HashMap<String, HashSet<Coord32>>,
    counter: usize,
    input_type: InputType,
    include_harmonics: bool,
) {
    let mut grid: HashMap<Coord32, &str> = HashMap::new();
    let mut imax: i32 = 0;
    let mut jmax: i32 = 0;
    for coord in coordinates {
        imax = cmp::max(imax, coord.x);
        jmax = cmp::max(jmax, coord.y);
        for (key, v) in &antennas {
            if v.contains(&coord) {
                grid.insert(coord, &key);
            }
        }
        if antinodes.contains(&coord) {
            grid.insert(coord, "#");
        }
    }
    let string = reconstruct_grid(grid, imax + 1, jmax + 1);
    write_string_to_file(
        &string,
        &format!(
            "./output_grids/output_{}_harmonics-{}_{:0>5}.txt",
            input_type, include_harmonics, counter
        ),
    );
}

fn main() {
    time_function(&part1);
    time_function(&part2);
}
