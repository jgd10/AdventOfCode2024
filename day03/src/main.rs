use aoc::get_input_as_lines;


fn parse() -> String{
    let data2: Vec<&str> = get_input_as_lines(include_str!("../input.txt"));
    data2.join("")
}

fn parse_chunk(first: &str) -> i32{
    let mut total: i32  = 0;
    if first.len() >= 3 && first.len() <= 7 && first.contains(",") {
        let numbers: Vec<&str> = first.split(",").collect();
        if numbers.len() == 2 {
            let mut multiplication: i32 = 1;
            let mut counter: i32 =0;
            //println!("{:?}", numbers);
            for num in numbers {
                if num.bytes().all(|c| c.is_ascii_digit()) {
                    let value: i32 = num.parse::<i32>().unwrap();
                    multiplication *= value;
                    counter += 1
                }
            if counter == 2 {
                total += multiplication;
            }
        }
    }

    }
    total
}


fn part1() {
    let line: String = parse();
    let chunks: Vec<&str> = line.split("mul(").collect();
    let mut total: i32 = 0;
    for chunk in chunks {
        if chunk.len() >= 4 {
            let Some((first, _)) = chunk.split_once(")") else {
                continue;
            };
            let multiplication = parse_chunk(first);
            total += multiplication;
        };
    };
    println!("Part 1: {}", total);
}

fn parse_super_chunk(chunk: &str) -> i32{
    let mut multiplication: i32 = 0;
    if chunk.len() >= 4 {
        let Some((first, _)) = chunk.split_once(")") else {
            return 0;
        };
        multiplication = parse_chunk(first);
    };
    multiplication
}

fn part2() {
    let line: String = parse();
    let chunks: Vec<&str> = line.split("don't()").collect();
    let mut new_chunks: Vec<&str> = Vec::new();
    let mut total: i32 = 0;
    new_chunks.push(chunks[0]);  // first chunk is enabled always
    for chunk in chunks.iter().skip(1) {
        let Some((_, last)) = chunk.split_once("do()") else { continue };
        new_chunks.push(last);
    }

    for new in new_chunks{
        if new.contains("mul("){
            let valid_blocks: Vec<&str> = new.split("mul(").collect();
            for block in valid_blocks {
                total += parse_super_chunk(block);
            }
        }
    }
    println!("Part 2: {}", total);
}

fn main() {
    part1();
    part2();
}
