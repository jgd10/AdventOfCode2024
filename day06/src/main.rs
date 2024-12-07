use std::collections::HashMap;
use std::collections::HashSet;
use std::hash::Hash;
use std::cmp;
use aoc::get_input_as_chars;
use aoc::Direction;
use aoc::Coord32;
use aoc::time_function;
use aoc::reconstruct_grid;
use aoc::write_string_to_file;
use aoc::InputType;



#[derive(Debug, Clone, Copy, Eq, PartialEq, PartialOrd, Ord, Hash)]
pub enum Tile {
    Space,
    Obstacle,
}


fn parse_input() -> (HashMap<Coord32, Tile>, Coord32){
    let lines: Vec<Vec<char>> = get_input_as_chars(include_str!("../input.txt"));
    let mut floor_plan: HashMap<Coord32, Tile> = HashMap::new();
    let mut guard: Coord32 = Coord32{x: -10, y: -10};
    for (j, row) in lines.iter().enumerate() {
        for (i, c) in row.iter().enumerate(){
            let coord: Coord32 = Coord32{x: i32::try_from(i).ok().unwrap(), y: i32::try_from(j).ok().unwrap()};
            let tile: Tile;
            match c {
                '#' => {tile = Tile::Obstacle;},
                '.' => {tile = Tile::Space;},
                '^' => {tile = Tile::Space; guard = coord;},
                _ => continue,
            };
            floor_plan.insert(coord, tile);
        }   
    }
    (floor_plan, guard)
}

fn patrol_guard(floor_plan: HashMap<Coord32, Tile>, mut guard: Coord32, mut direction: Direction) -> bool{
    let mut prev_states: HashMap<(Coord32, Direction), usize> = HashMap::new();
    let min_repeats: usize = 3;
    while floor_plan.contains_key(&guard) {
        if !prev_states.contains_key(&(guard, direction)){
            prev_states.insert((guard, direction), 1);
        }
        else {
            let value = prev_states.get(&(guard, direction)).unwrap();
            prev_states.insert((guard, direction), value + 1);
        }
        let next_space = guard.get_next_coord(direction);
        match floor_plan.get(&next_space) {
            Some(Tile::Obstacle) => direction = direction.turn_clockwise(),
            Some(Tile::Space) => guard = next_space,
            _ => guard = next_space,
        }
        if prev_states.contains_key(&(guard, direction)) && prev_states.get(&(guard, direction)).unwrap() >= &min_repeats {
            return true
        }
    }
    false
}


fn visualise_floorplan(floor_plan: HashMap<Coord32, Tile>, guard: Coord32, direction: Direction, visited: HashSet<Coord32>, index: usize, input_type: InputType) {
    let mut text_grid: HashMap<Coord32, &str> = HashMap::new();
    let mut imax: i32 = 0;
    let mut jmax: i32 = 0;
    for (coord, tile) in floor_plan {
        text_grid.insert(coord, match tile { Tile::Obstacle => "#", Tile::Space => "." });
        imax = cmp::max(imax, coord.x);
        jmax = cmp::max(jmax, coord.y);
    }
    for v in visited {
        text_grid.insert(v, "o");
    }
    let guard_icon: &str = match direction {Direction::East => ">", Direction::North => "^", Direction::South => "v", Direction::West => "<"};
    text_grid.insert(guard, guard_icon);
    let string = reconstruct_grid(text_grid, imax+1, jmax+1);
    write_string_to_file(&string, &format!("./output_{}_{:0>5}.txt", input_type, index));
}


fn part1(){
    let (floor_plan, mut guard) = parse_input();
    let mut visited_tiles: HashSet<Coord32> = HashSet::new();
    let mut direction: Direction = Direction::North;
    let mut counter: usize = 0;
    let input_type = InputType::Input;
    while floor_plan.contains_key(&guard) {
        visualise_floorplan(floor_plan.clone(), guard, direction, visited_tiles.clone(), counter, input_type);
        visited_tiles.insert(guard);
        let next_space = guard.get_next_coord(direction);
        match floor_plan.get(&next_space) {
            Some(Tile::Obstacle) => direction = direction.turn_clockwise(),
            Some(Tile::Space) => guard = next_space,
            _ => guard = next_space,
        }
        counter += 1;
    }
    println!("Part 1 {}", visited_tiles.len())
}
    

fn part2(){
    let (floor_plan, mut guard) = parse_input();
    let mut direction: Direction = Direction::North;
    let mut banned_locations: HashSet<Coord32> = HashSet::new();
    let mut new_placements: HashSet<Coord32> = HashSet::new();
    banned_locations.insert(guard);
    for (key, value) in floor_plan.clone().into_iter() {
        if value == Tile::Obstacle{
            banned_locations.insert(key);
        }
    }
    while floor_plan.contains_key(&guard) {
        banned_locations.insert(guard);
        let next_space = guard.get_next_coord(direction);
        if floor_plan.contains_key(&next_space) && !banned_locations.contains(&next_space){
            let mut trial_floor_plan: HashMap<Coord32, Tile> = floor_plan.clone();
            trial_floor_plan.insert(next_space, Tile::Obstacle);
            if patrol_guard(trial_floor_plan, guard, direction) {
                banned_locations.insert(next_space);
                new_placements.insert(next_space);
            }
        }
        else {
            // println!("You can't park there mate! {:?}", next_space);
        }
        match floor_plan.get(&next_space) {
            Some(Tile::Obstacle) => direction = direction.turn_clockwise(),
            Some(Tile::Space) => guard = next_space,
            _ => guard = next_space,
        }
    }
    println!("Part 2 {}", new_placements.len());
}


fn main() {
    time_function(&part1);
    time_function(&part2);
}
