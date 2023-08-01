import {useState} from 'react';

function Question(props){
    const [displayAnswer, setDisplayAnswer] = useState(false)
    const [correctAnswer, setCorrectAnswer] = useState(false)
    const [explanation, setExplanation] = useState("")

    // check users answer, change score, and display correct answers
    const checkAnswer = (key)=>{
        setDisplayAnswer(true);
        setExplanation(props.question.explanation)


        if (props.question.answerChoices[key].correctAnswer){
            setCorrectAnswer(true)
            props.setScore((score)=>{return score+1})
        }  
        else{
            setCorrectAnswer(false)
        }
    }


    return(
        <div className="questionSlide">

            {displayAnswer ? <p className="question">{props.index + 1}. {props.question.question}</p> 
            :
            <p className="question">{props.index + 1}. {props.question.question}</p> 
            }

            {/* Show answer choices */}
            {Object.keys(props.question.answerChoices).map((key, index)=>{

                return (
                    <>
                        {displayAnswer ? 

                            <div key={index} style={props.question.answerChoices[key].correctAnswer ? {'backgroundColor': 'rgb(146, 226, 202)'} : {'backgroundColor': 'rgb(255, 137, 137)'}} className="answerChoiceSlides">
                                <p> {key}. {props.question.answerChoices[key].answerChoice}</p>
                            </div>:

                            <div key={index} className="answerChoiceSlides" onClick={()=>{checkAnswer(key)}}>

                                <p> {key}. {props.question.answerChoices[key].answerChoice}</p>
                            </div>
                        }
                    </>
                  );
            })}
            <p className="explanation">{explanation}</p>
        </div>
    )
}

export default Question