import axios from 'axios';

export async function getQuestions({role, yearsOfExperience,numOfQuestions}){
    return axios.get('/questions', {role, yearsOfExperience,numOfQuestions});
}