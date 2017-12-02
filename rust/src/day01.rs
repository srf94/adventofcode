use std::env;
use std::fs::File;
use std::io::prelude::*;


fn main() {
	let filename = "../../input/day01.txt";
    let mut f = File::open(filename).expect("file not found");
    let mut data = String::new();
    f.read_to_string(&mut data)
        .expect("something went wrong reading the file");

    let input: Vec<_> = data
        .chars()
        .filter_map(|c| c.to_digit(10))
        .collect();

    let N = input.len();

    let mut sum = 0;
    for i in 0..N {
    	if input[i] == input[(i+1) % N] {
    		sum += input[i];
    	}
    }

    println!("Part 1: {:?}", sum);

    let mut sum = 0;
    for i in 0..N {
    	if input[i] == input[(i+N/2) % N] {
    		sum += input[i];
    	}
    }

    println!("Part 2: {:?}", sum);

}
