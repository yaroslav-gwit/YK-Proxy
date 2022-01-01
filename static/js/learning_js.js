// add to body <script src="{% static 'js/chart.js' %}"></script>
// Variables
let name1 = 'John';
console.log(name1);


// String, Numbers, Boolean, null, undefined
let name = 'John';
let age = 30;
const rating = 4.5;
const isCool = true;
const x = null;
const y = undefined;
let z;

console.log(name, age, isCool);
console.log(typeof rating);


// Cancatination
console.log('My name is', name, 'and I am', age);


// Template String
console.log(`My name is ${name} and I am ${age}`);


// Using default methods
const s = 'Hello World';
console.log(s.length);
console.log(s.toUpperCase());
console.log(s.toLowerCase());
console.log(s.substring(0, 5));
console.log(s.substring(0, 5).toUpperCase());

const xTags = 'technology, computers, it, code';
console.log(xTags.split(", "));


// Arrays
const numbers = new Array(1,2,3,4,5,6,7,8);
console.log(numbers);

const fruits = ['apples', 'oranges', 'pears', 'bananas', ];
fruits[3] = 'grapes';
fruits.push('mangos');
fruits.unshift('strawberries');
fruits.pop();

console.log(fruits);
console.log(fruits[1]);
console.log(Array.isArray(fruits));
console.log(fruits.indexOf('oranges'))


// Object literals
const person = {
    firstName: 'John',
    lastName: 'Doe',
    age: 30,
    hobbies: [
        'it',
        'sports',
        'gaming',
    ],
    address: {
        street: '2 Devon Pl',
        city: 'Boston',
        state: 'NY'
    }
};

console.log(person);
console.log(person.firstName);
console.log(person.hobbies);
console.log(person.hobbies[2]);

// const { firstName, lastName } = person;
const { firstName, lastName, address: { city } } = person;
console.log(firstName, lastName, city);

person.email = 'john@doe.com';
console.log(person);


// Working with arrays
const todos = [
    {
        id: 1,
        text: 'take out trash',
        isCompleted: true,
    },
    {
        id: 2,
        text: 'walk the dog',
        isCompleted: true,
    },
    {
        id: 3,
        text: 'wash clothes',
        isCompleted: false,
    }
];

console.log(todos);
console.log(todos[1].text)

const todoJSON = JSON.stringify(todos);
console.log(todoJSON);

for (let i = 0; i < todos.length; i = i + 1) {
    console.log(`${todos[i].id}. ${todos[i].text}`)
}

for (let todo of todos) {
    console.log(`${todo.id}. ${todo.text}`)
}


// for loops
console.log('For loop')
for (let i = 0; i < 10; i = i + 1) {
    console.log(i);
}

// while loops
let i = 0;
console.log('While loop')
while(i < 10) {
    console.log(i)
    i = i + 1
}

// forEach, map, filter
todos.forEach(function(todo) {
    console.log(todo.text)
}
);