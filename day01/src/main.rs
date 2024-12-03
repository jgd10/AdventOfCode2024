use aoc::get_input_as_lines;
use itertools::Itertools;
use std::convert::TryFrom;


fn parse_input() -> (Vec<i32>, Vec<i32>){
    let lines: Vec<&str> = get_input_as_lines(include_str!("../example.txt"));
    let mut left_nums: Vec<i32> = Vec::new();
    let mut right_nums: Vec<i32> = Vec::new();
    for line in lines {
        let nums: Vec<i32> = line.split("   ").map(|x|->i32{x.parse().unwrap()}).collect();
        left_nums.push(nums.clone()[0]);
        right_nums.push(nums.clone()[1]);
    }
    left_nums.sort();
    right_nums.sort();
    (left_nums, right_nums)
}

fn part1() {
    let mut total_distance: u32 = 0;
    let (left_nums, right_nums) = parse_input();
    for (left, right) in left_nums.iter().zip(right_nums.iter()){
        total_distance += left.abs_diff(*right);
    }
    println!("Part 1: {}", total_distance);
}

fn part2() {
    let (left_nums, right_nums) = parse_input();
    let mut right_counts: std::collections::HashMap<i32, usize> = right_nums.into_iter().counts();
    let mut total_count: usize = 0;
    for num in left_nums {
        total_count += usize::try_from(num).ok().unwrap() * *right_counts.entry(num).or_insert(0);
    }
    println!("Part 2: {}", total_count);
}


fn main() {
    part1();
    part2();
}