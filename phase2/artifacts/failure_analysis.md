# Failure Analysis

## Purpose
This file records what the raw baseline gets wrong.

## Failure Categories
- Missing context 
- Poor prompting
- Weak safety handling
- Poor task decomposition
- Other

## Test Case 1
**Main issue:** The suggestions that it provides to the users prompt is very generic 
**Failure category:** Poor prompting
**Why it matters:** The suggestions being given to the user must be easy to work on for the user . If the output is very vauge ,  enhancing the system to perform better becomes a difficult task . .

## Test Case 2
**Main issue:** While it uses some personalization , it is still generic as compared to what the situation of the user might be
**Failure category:**  Missing context 
**Why it matters:** It has very long and vauge plans and this does not suit college students who might have extremely busy schedules .

## Test Case 3
**Main issue:** It has a lot of details for a minor issue which can get overwhelming for the user . It does not directly emphasize on the easiest next step the user can take to tackle their problems effectively .
**Failure category:** Weak safety handling
**Why it matters:** Having improper answers for injury related problems can also include suggestions of excercises that can increase the pain due to injuries . It is important for the model to handle injury related discussions very carefully .

## Test Case 4
**Main issue:** Lacking a strong connection to the student specific problem 
**Failure category:** Missing context 
**Why it matters:** While it does give a 15 minute workout idea , it does not give ideas based on the fact that students who are busy are likely to have other struggles like having limited space to perform the activites , not being able to buy the equipment they need for the exercises etc . These problems are not being taken into account in the baseline suggestions .

## Test Case 5
**Main issue:** The user's immediate need is not met with a viable solution but rather a routine involving different types of exercises . 
**Failure category:** Poor task decomposition
**Why it matters:** It is important to ensure that users are being given valid thoughtful solutions for their problems rather than a rushed routine that is not related to what the user actually needs . This is unhelpful for the users .
