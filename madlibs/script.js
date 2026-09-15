/*
  document.getElementById(ELEMENT_ID) is how we access the HTML on the page.
  These variables are used to manipulate the HTML by showing or hiding pieces.
*/
var storyDiv = document.getElementById("theStory");
var wordsDiv = document.getElementById("words");
var form = document.getElementById("wordInput");
var resetButton = document.getElementById("reset");

function tellStory() {
  // Here, we are getting the value of the input element by the ID.
  // Get the value of all of the other variables in the same way.
  var name = document.getElementById("name").value;
  var place = document.getElementById("place").value;
  var number = document.getElementById("number").value;
  var time = document.getElementById("time").value;
  var animal = document.getElementById("animal").value;
  var adjective = document.getElementById("adjective").value;
  var friend = document.getElementById("friend").value;

  /*
    What if you get a unit of time that should be plural? Or what if you get a
    plural unit of time that should be singular? This function will check both
    the submitted number and time to make sure they match so the story makes sense.
  */
  time = checkNumber(number, time);

  var story = `<p>Once upon a time, ${name} was walking to ${place}. It felt like ${name}
  had been walking forever but really it was ${number} ${time}. Suddenly a talking
  ${animal} appeared and asked ${name} where they were going. </p>`;

  story += `<p>${name} didn't trust this ${animal} because of their ${adjective} eyes and besides,
  everyone knows not to trust a talking ${animal}. ${name} ignored the ${animal} and kept
  walking until they saw their friend ${friend}.</p>`;

  storyDiv.classList.remove("hidden");
  storyDiv.innerHTML = story;

  wordsDiv.classList.add("hidden");
  resetButton.classList.remove("hidden");
}

function checkNumber(number, word) {
  if (number == 1 && word.slice(-1) != "s") {
    // if number is NOT 1 and the word does NOT end in s, add an s
    word += "s";
  } else if (number == 1 && word.slice(-1) == "s") {
    // if the number is 1 & the word DOES end in s, remove it
    word = word.slice(0, -1);
  }

  // The word needs to be returned because it might have changed.
  return word;
}

function resetStory() {
  /*
    This function resets the inputs back to blank and shows the inputs, and it
    hides the story and the reset button.
  */
  form.reset();
  wordsDiv.classList.remove("hidden");

  storyDiv.classList.add("hidden");
  resetButton.classList.add("hidden");
}
