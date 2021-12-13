const start = document.getElementById('start')
const question = document.getElementById('question')
const next = document.getElementById('next')


let questionApres



start.addEventListener('click', lancer);
next.addEventListener('click', () => {
  currentQuestionIndex++
  prochaineQuestion()
})

function lancer {
	console.log('Lancement du jeu') 
	start.classList.add('hide')
	question.classList.remove('hide')
	prochaineQuestion()
}