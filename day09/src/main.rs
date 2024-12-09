use aoc::get_input_as_chars;
use aoc::InputType;
use aoc::time_function;


fn parse(input_type: InputType) -> Vec<Vec<usize>>{
    let characters: Vec<char> = match input_type {
        InputType::Input => get_input_as_chars(include_str!("../input.txt")).get(0).unwrap().clone(),
        InputType::Example
        | InputType::Example2
        | InputType::Test
        | InputType::Test1
        | InputType::Test2
        | InputType::Test3 => get_input_as_chars(include_str!("../example.txt")).get(0).unwrap().clone(),
        InputType::Example1 => get_input_as_chars(include_str!("../example1.txt")).get(0).unwrap().clone(),
    };
    let mut disk: Vec<Vec<usize>> = Vec::new();
    let mut counter: usize = 0;
    for (i, character) in characters.iter().enumerate() {
        let block: Vec<usize>;
        if i % 2 == 0{
            block = vec![counter+1; character.to_digit(10).unwrap() as usize];
            counter += 1;
        }
        else {
            block = vec![0; character.to_digit(10).unwrap() as usize];
        }
        disk.push(block);
    }
    disk
}


fn part1(){
    let mut disk: Vec<Vec<usize>> = parse(InputType::Example);
    let mut last_block: Vec<usize> = disk.pop().unwrap();
    let mut first_block: &Vec<usize> = disk.get(0).unwrap();
    while last_block[0] == 0 {
        last_block = disk.pop().unwrap();
    }
    while first_block[0] != 0 {

    }
}


fn part2(){

}


fn main() {
    time_function(&part1);
    time_function(&part2);
}
