use aoc::get_input_as_lines;


fn parse_input() -> Vec<Vec<i32>>{
    let lines: Vec<&str> = get_input_as_lines(include_str!("../example.txt"));
    let mut rows: Vec<Vec<i32>> = Vec::new();
    for line in lines {
        let nums: Vec<i32> = line.split(" ").map(|x|->i32{x.parse().unwrap()}).collect();
        rows.push(nums);
    }
    rows
}


fn check_line_safe(line: Vec<i32>) -> bool {
    let mut prev_element: &i32 = &line[0];
    let mut safe: bool = true;
    if prev_element.abs() == 0 || prev_element.abs() > 3 {
        safe = false;
    }
    for diff in line.iter().skip(1) {
        if diff.abs() == 0 || diff.abs() > 3 {
            safe = false;
        }
        if (prev_element < &0 && diff > &0) || (prev_element > &0 && diff < &0){
            safe = false;
        }
        prev_element = diff;
    }
    safe
}

fn get_line_differences(line: Vec<i32>) -> Vec<i32> {
    let mut diffs: Vec<i32> = Vec::new();
    let mut start: &i32 = &line[0];
    for number in line.iter().skip(1) {
        diffs.push(number - start);
        start = number;

    }
    diffs
}


fn part1(){
    let data: Vec<Vec<i32>> = parse_input();
    let mut safe_count: i32 = 0;
    for line_ in data {
        let diffs: Vec<i32> = get_line_differences(line_.clone());
        if check_line_safe(diffs.clone()){
            safe_count += 1;
        }
    }
    println!("Part 1: {}", safe_count)
}

fn check_tolerance(line: Vec<i32>) -> bool {
    let mut safe: bool = false;
    for (i, _) in line.iter().enumerate() {
        let mut new_line: Vec<i32> = line.clone();
        new_line.remove(i);
        let diffs: Vec<i32> = get_line_differences(new_line.clone());
        safe = check_line_safe(diffs.clone());
        if safe {
           break 
        }
    }
    safe
}


fn part2(){
    let data: Vec<Vec<i32>> = parse_input();
    let mut safe_count: i32 = 0;
    let mut safe: bool;
    for line_ in data {
        let diffs: Vec<i32> = get_line_differences(line_.clone());
        safe = check_line_safe(diffs.clone());
        if !safe {
            safe = check_tolerance(line_.clone());
        }
        if safe {
            safe_count += 1;
        }
    }
    println!("Part 2: {}", safe_count)
}

fn main() {
    part1();
    part2();
}
