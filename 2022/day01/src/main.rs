// https://github.com/timvisee/advent-of-code-2022/blob/master/day01a/src/main.rs
fn part1(payload: &str) -> u32 {
    let data = payload
            .split("\n\n")
            .map(|e| e.lines().map(|c| c.parse::<u32>().unwrap()).sum::<u32>())
            .max()
            .unwrap();
    data
}

// https://github.com/timvisee/advent-of-code-2022/blob/master/day01b/src/main.rs
fn part2(payload: &str) -> u32 {
    let mut cals = payload
            .split("\n\n")
            .map(|e| e.lines().map(|c| c.parse::<u32>().unwrap()).sum::<u32>())
            .collect::<Vec<u32>>();
    cals.sort_unstable();
    let result = cals.into_iter().rev().take(3).sum();
    println!("{:?}", result);
    result
}

fn main() {
    let payload = include_str!("../input.txt");
    println!("part1={:?}", part1(payload));
    println!("part2={:?}", part2(payload));
}
