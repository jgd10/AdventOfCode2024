use std::collections::HashMap;
use std::fs::File;
use std::fs::write;
use std::io::LineWriter;
use std::io::Write;
use std::time::Instant;
use std::fmt;


pub fn reconstruct_grid(coords: HashMap<Coord32, &str>, imax: i32, jmax: i32) -> String {
    let mut grid: Vec<Vec<&str>> = vec![vec!["."; imax as usize]; jmax as usize];
    let mut rows: Vec<String> = Vec::new();
    for (c, s) in coords {
        grid[c.y as usize][c.x as usize] = s;
    }
    for row in grid {
        rows.push(row.join(""));
    }
    rows.join("\n")
}


pub fn write_string_to_file(string: &str, filepath: &str) {
    write(filepath, string).expect("Failed to write to file");
}

pub fn time_function(func: &dyn Fn()){
    let now = Instant::now();
    func();
    println!("{:?}", now.elapsed());
}



pub fn write_vector_to_text_file<T: std::fmt::Debug>(my_vector: Vec<T>){
    let file = File::create("my_vector.txt").unwrap();
    let mut file = LineWriter::new(file);
    for coord in my_vector {
        write!(file, "{:?}\n", coord).ok();
    }
    file.flush().unwrap();
}

#[derive(Debug, Clone, Copy, Eq, PartialEq, PartialOrd, Ord, Hash)]
#[allow(dead_code)]
pub enum InputType {
    Input,
    Example,
    Example1,
    Example2,
    Test,
    Test1,
    Test2,
    Test3,
}

impl fmt::Display for InputType {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            InputType::Input => write!(f, "input"),
            InputType::Example => write!(f, "example"),
            InputType::Example1 => write!(f, "example1"),
            InputType::Example2 => write!(f, "exampl2"),
            InputType::Test => write!(f, "test"),
            InputType::Test1 => write!(f, "test1"),
            InputType::Test2 => write!(f, "test2"),
            InputType::Test3 => write!(f, "test3"),
        }
    }
}


#[derive(Debug, Clone, Copy, Eq, PartialEq, PartialOrd, Ord, Hash)]
#[allow(dead_code)]
pub enum Direction {
    North,
    South,
    East,
    West,
}

impl Direction {
    #[allow(dead_code)]
    pub fn turn_clockwise(self) -> Direction{
        match self {
            Direction::East => Direction::South,
            Direction::West => Direction::North,
            Direction::North => Direction::East,
            Direction::South => Direction::West,
        }
    }
    #[allow(dead_code)]
    pub fn turn_anticlockwise(self) -> Direction{
        match self {
            Direction::East => Direction::North,
            Direction::West => Direction::South,
            Direction::North => Direction::West,
            Direction::South => Direction::East,
        }
    }
} 




#[derive(Debug, Clone, Copy, Eq, PartialEq, PartialOrd, Ord, Hash)]
#[allow(dead_code)]
pub struct Coord32 {
    pub x: i32,
    pub y: i32,
}

impl Coord32 {
    #[allow(dead_code)]
    pub fn get_next_coord(self, direction: Direction) -> Coord32 {
        match direction {
            Direction::East => Coord32{x: self.x + 1, y: self.y},
            Direction::West => Coord32{x: self.x - 1, y: self.y},
            Direction::North => Coord32{x: self.x, y: self.y - 1},
            Direction::South => Coord32{x: self.x, y: self.y + 1},
        }
    }
}


#[derive(Debug, Clone, Copy, Eq, PartialEq, PartialOrd, Ord, Hash)]
#[allow(dead_code)]
pub struct Coord64 {
    pub x: i64,
    pub y: i64,
}

// Uses a rule I found by accident: get the total area using the shoelace algorithm (the trapezoid formula in this case)
// Then add that to half the total perimeter and add 1.
// Taken from 2023 day 18 - only works for polygon with either horizontal or vertical edges (i.e. squares)
#[allow(dead_code)]
fn calculate_area_polygon32(coordinates: Vec<Coord32>) -> i32{
    let mut total: i32 = 0;
    for i in 0..(coordinates.len()-1){
        let amount = (coordinates[i].y + coordinates[i+1].y)*(coordinates[i].x - coordinates[i+1].x);
        total += amount;
    }
    total += (coordinates[coordinates.len()-1].y + coordinates[0].y)*(coordinates[coordinates.len()-1].x - coordinates[0].x);
    total.abs() / 2 + calculate_perimeter32(coordinates) / 2 + 1
}


// Taken from 2023 day 18 - only works for polygon with either horizontal or vertical edges
#[allow(dead_code)]
fn calculate_area_polygon64(coordinates: Vec<Coord64>) -> i64{
    let mut total: i64 = 0;
    for i in 0..(coordinates.len()-1){
        let amount = (coordinates[i].y + coordinates[i+1].y)*(coordinates[i].x - coordinates[i+1].x);
        total += amount;
    }
    total += (coordinates[coordinates.len()-1].y + coordinates[0].y)*(coordinates[coordinates.len()-1].x - coordinates[0].x);
    total.abs() / 2 + calculate_perimeter64(coordinates) / 2 + 1
}

// Taken from 2023 day 18 - only works for polygon with either horizontal or vertical edges
#[allow(dead_code)]
fn calculate_perimeter32(coordinates: Vec<Coord32>) -> i32 {
    let mut total: i32 = 0;
    for i in 0..(coordinates.len()-1){
        let amount = (coordinates[i].y - coordinates[i+1].y)+(coordinates[i].x - coordinates[i+1].x);
        total += amount;
    }
    total += (coordinates[coordinates.len()-1].y + coordinates[0].y)*(coordinates[coordinates.len()-1].x - coordinates[0].x);
    total
}

// Taken from 2023 day 18 - only works for polygon with either horizontal or vertical edges
#[allow(dead_code)]
fn calculate_perimeter64(coordinates: Vec<Coord64>) -> i64 {
    let mut total: i64 = 0;
    for i in 0..(coordinates.len()-1){
        let amount = (coordinates[i].y - coordinates[i+1].y)+(coordinates[i].x - coordinates[i+1].x);
        total += amount;
    }
    total += (coordinates[coordinates.len()-1].y + coordinates[0].y)*(coordinates[coordinates.len()-1].x - coordinates[0].x);
    total
}

#[allow(dead_code)]
pub fn get_input_as_lines(input: &'static str) -> Vec<&'static str>{
    let mut data: Vec<&str> = Vec::new();
    for line in input.lines() {
        data.push(line)
    }
    data
}

#[allow(dead_code)]
pub fn get_input_as_chars(input: &str) -> Vec<Vec<char>>{
    let mut char_vec: Vec<char>;
    let mut data: Vec<Vec<char>> = Vec::new();
    for line in input.lines() {
        char_vec = line.chars().collect();
        data.push(char_vec)
    }
    data
}

#[allow(dead_code)]
pub fn parse_collection_of_strings_to_usize(input: Vec<&str>) -> Vec<usize>{
    input.iter().map(|x: &&str| {x.parse().unwrap()}).collect()
}


#[allow(dead_code)]
pub fn parse_collection_of_strings_to_i32(input: Vec<&str>) -> Vec<i32>{
    input.iter().map(|x: &&str| {x.parse().unwrap()}).collect()
}


#[allow(dead_code)]
pub fn parse_collection_of_strings_to_i64(input: Vec<&str>) -> Vec<i64>{
    input.iter().map(|x: &&str| {x.parse().unwrap()}).collect()
}