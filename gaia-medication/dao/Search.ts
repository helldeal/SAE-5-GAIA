import { getAllMed } from "./Meds";

function findMostAccurateMed(meds: any[], search: string) {
  const scores = meds.map((med) => {
    const name = med.Name.toLowerCase();
    const s = search.toLowerCase();
    const index = name.indexOf(s);
    if (index === -1) {
      return 0;
    } else if (index === 0) {
      return s.length / name.length;
    } else {
      return s.length / (name.length + index);
    }
  });
  const medScores = meds.map((med, index: string | number) => {
    return {
      Name: med.Name,
      CIS: med.CIS,
      score: scores[index],
    };
  });
  const sortedMeds = medScores.sort(
    (a: { score: number }, b: { score: number }) => b.score - a.score
  );
  return sortedMeds.filter(med=>med.score>0)//.map((med: { Name: any }) => med.Name);
}

export function searchMed(inputText: string, maxResults = 20) {
  const medicaments = getAllMed();
  // Calcul de la distance pour chaque médicament et tri par proximité
  return findMostAccurateMed(medicaments, inputText).slice(0, maxResults);
}