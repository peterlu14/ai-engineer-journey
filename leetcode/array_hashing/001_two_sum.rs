// 001. Two Sum
// https://leetcode.com/problems/two-sum/
// 難度：Easy
//
// 給一個整數陣列 nums 和目標值 target
// 找出兩個數字的 index，使它們相加等於 target
// 每個 input 只有一個答案，不能用同一個元素兩次
//
// Example:
//   Input:  nums = [2, 7, 11, 15], target = 9
//   Output: [0, 1]  (nums[0] + nums[1] = 2 + 7 = 9)

use std::collections::HashMap;

// fn two_sum(nums: Vec<i32>, target: i32) -> Vec<i32> {
//     for (i, &num) in nums.iter().enumerate() {
//         for (j, &num2) in nums.iter().enumerate() {
//             if i != j && num + num2 == target {
//                 return vec![i as i32,j as i32]
//             }
//         }
//     }
//     return vec![]
// }

fn two_sum(nums: Vec<i32>, target: i32) -> Vec<i32> {
    let mut map = HashMap::new();
    for (i, &num) in nums.iter().enumerate() {
        let diff = target - num;
        if let Some(&j) = map.get(&diff) {
            return vec![j as i32, i as i32]
        }
        map.insert(num, i);
    }
    vec![]
}

fn main() {
    println!("{:?}", two_sum(vec![2, 7, 11, 15], 9));  // [0, 1]
    println!("{:?}", two_sum(vec![3, 2, 4], 6));        // [1, 2]
    println!("{:?}", two_sum(vec![3, 3], 6));            // [0, 1]
}