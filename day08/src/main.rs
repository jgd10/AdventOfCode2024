use std::collections::HashMap;
use std::collections::HashSet;
use itertools::Itertools;
use std::cmp;

use aoc::get_input_as_chars;
use aoc::Coord32;
use aoc::time_function;
use aoc::reconstruct_grid;


fn parse() -> (HashSet<Coord32>, HashMap<String, HashSet<Coord32>>){
    let mut coordinates: HashSet<Coord32> = HashSet::new();
    let mut antennas: HashMap<String, HashSet<Coord32>> = HashMap::new();
    let characters: Vec<Vec<char>> = get_input_as_chars(include_str!("../example.txt"));
    for (j, row) in characters.iter().enumerate() {
        for (i, col) in row.iter().enumerate() {
            let coordinate: Coord32 = Coord32{ x: i as i32, y: j as i32 };
            coordinates.insert(coordinate);
            match col {
                '.' => continue,
                _ => {
                    let existing: &mut HashSet<Coord32> = antennas.entry(col.to_string()).or_insert(HashSet::new());
                    existing.insert(coordinate);
                },
            }
        }
    }
    (coordinates, antennas)
}


fn get_antinode_coords(coord1: &Coord32, coord2: &Coord32, allowed: &HashSet<Coord32>, repeats: i32) -> HashSet<Coord32> {
    let difference_vector: Coord32 = Coord32 { x: coord1.x - coord2.x, y: coord1.y - coord2.y };
    let mut antinodes: HashSet<Coord32> = HashSet::new();
    let mut furthest_coord: Coord32;
    let mut counter: i32 = 0;
    // go forward
    furthest_coord = Coord32{x: coord1.x + difference_vector.x, y: coord1.y + difference_vector.y};
    while allowed.contains(&furthest_coord) && counter < repeats{
        antinodes.insert(furthest_coord);
        furthest_coord = Coord32{x: furthest_coord.x + difference_vector.x, y: furthest_coord.y + difference_vector.y};
        counter += 1;
    }
    // go backward
    counter = 0;
    furthest_coord = Coord32{x: coord2.x - difference_vector.x, y: coord2.y - difference_vector.y};
    while allowed.contains(&furthest_coord) && counter < repeats{
        antinodes.insert(furthest_coord);
        furthest_coord = Coord32{x: furthest_coord.x - difference_vector.x, y: furthest_coord.y - difference_vector.y};
        counter += 1;
    }
    return antinodes
}


fn part1() {
    let (coordinates, antennas) = parse();
    let mut antinodes: HashSet<Coord32> = HashSet::new();
    for (_, coords) in antennas {
        for coord1 in coords.clone() {
            for coord2 in &coords {
                if &coord1 != coord2 {
                    let antinode_set = get_antinode_coords(&coord1, coord2, &coordinates, 1);
                    for antinode in antinode_set{
                        antinodes.insert(antinode);
                    }
                }
            }
        }
    }
    println!("Part 1: {}", antinodes.len());
}

fn part2() {
    let (coordinates, antennas) = parse();
    let mut antinodes: HashSet<Coord32> = HashSet::new();
    for (_, coords) in &antennas {
        for coord1 in coords.clone() {
            for coord2 in coords {
                if &coord1 != coord2 {
                    let antinode_set = get_antinode_coords(&coord1, coord2, &coordinates, 999);
                    antinodes.insert(coord1);
                    antinodes.insert(*coord2);
                    for antinode in antinode_set{
                        antinodes.insert(antinode);
                    }
                }
            }
        }
    }

    visualise(coordinates, antinodes.clone(), antennas);
    println!("Part 2: {}", antinodes.len());
}


fn visualise(coordinates: HashSet<Coord32>, antinodes: HashSet<Coord32>, antennas: HashMap<String, HashSet<Coord32>>){
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
        if antinodes.contains(&coord){
            grid.insert(coord, "#");
        }
    }
    let string = reconstruct_grid(grid, imax+1, jmax+1);
    println!("{}", string);
}

fn main() {
    time_function(&part1);
    time_function(&part2);
}
