import data from './medication.json';

export async function getAllMed(){   
  try {
    const medicaments=JSON.parse(JSON.stringify(data))
    return medicaments
  } catch (error) {
    console.error('Error reading JSON file', error);
  }
}
