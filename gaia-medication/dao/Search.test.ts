import { searchMed, SearchAllergy, trouverNomMedicament } from './Search';

describe('Search Tests', () => {
    describe('searchMed', () => {
        it('should return the most accurate medication based on search string', () => {
            const mockMeds = [
                { name: 'Aspirin'},
                { name: 'Paracetamol'},
            ];

            jest.mock('./Meds', () => ({
                getAllMed: () => mockMeds
            }));
            const expectApsi=[
                    {
                        "CIS": 63825628,
                        "Name": "METASPIRINE, comprimé",
                        "score": 0.16666666666666666,
                        "type": "comprimé",
                    },
                    {
                        "CIS": 68799614,
                        "Name": "ASPIRINE DU RHÔNE 500 mg, comprimé",
                        "score": 0.11764705882352941,
                        "type": "comprimé",
                    },
                    {
                        "CIS": 65265765,
                        "Name": "ASPIRINE UPSA 500 mg, comprimé effervescent",
                        "score": 0.09302325581395349,
                        "type": "comprimé effervescent(e)",
                    },
                    {
                        "CIS": 69029253,
                        "Name": "ASPIRINE DU RHONE 500 mg, comprimé à croquer",
                        "score": 0.09090909090909091,
                        "type": "comprimé à croquer",
                    },
                    {
                        "CIS": 69781373,
                        "Name": "ASPIRINE pH 8 500 mg, comprimé gastro-résistant",
                        "score": 0.0851063829787234,
                        "type": "comprimé gastro-résistant(e)",
                    },
                    {
                        "CIS": 61946403,
                        "Name": "ASPIRINE ARROW 100 mg, comprimé gastro-résistant",
                        "score": 0.08333333333333333,
                        "type": "comprimé gastro-résistant(e)",
                    },
                    {
                        "CIS": 61464022,
                        "Name": "ASPIRINE PROTECT 100 mg, comprimé gastro-résistant",
                        "score": 0.08,
                        "type": "comprimé gastro-résistant(e)",
                    },
                    {
                        "CIS": 64872883,
                        "Name": "ASPIRINE PROTECT 300 mg, comprimé gastro-résistant",
                        "score": 0.08,
                        "type": "comprimé gastro-résistant(e)",
                    },
                    {
                        "CIS": 64849094,
                        "Name": "NOVACETOL (ASPIRINE PARACETAMOL), comprimé",
                        "score": 0.07547169811320754,
                        "type": "comprimé",
                    },
                    {
                        "CIS": 62358794,
                        "Name": "ASPIRINE 500 mg VITAMINE C OBERLIN, comprimé effervescent",
                        "score": 0.07017543859649122,
                        "type": "comprimé effervescent(e)",
                    },
                    {
                        "CIS": 61137191,
                        "Name": "ANTIGRIPPINE A L'ASPIRINE ETAT GRIPPAL, comprimé",
                        "score": 0.06153846153846154,
                        "type": "comprimé",
                    },
                    {
                        "CIS": 61172160,
                        "Name": "ASPIRINE UPSA TAMPONNEE EFFERVESCENTE 1000 mg, comprimé effervescent",
                        "score": 0.058823529411764705,
                        "type": "comprimé effervescent(e)",
                    },
                    {
                        "CIS": 67831952,
                        "Name": "ASPIRINE UPSA VITAMINEE C TAMPONNEE EFFERVESCENTE, comprimé effervescent",
                        "score": 0.05555555555555555,
                        "type": "comprimé effervescent(e)",
                    },
                    {
                        "CIS": 65057344,
                        "Name": "ASPIDIUM FILIX MAS BOIRON, degré de dilution compris entre 4CH et 30CH ou entre 7DH et 60DH",
                        "score": 0.04395604395604396,
                        "type": " comprimé et solution(s) et granules et poudre et pommade",
                    }
                ]
            const searchString = 'Aspi';
            const result = searchMed(searchString);
            expect(result).toEqual(expectApsi);
        });

    });

    describe('SearchAllergy', () => {
        it('should return the most accurate allergy based on search string', () => {
            const mockMeds = [
                { name: 'Aspirin'},
                { name: 'Paracetamol'},
            ];

            jest.mock('./Meds', () => ({
                getAllMed: () => mockMeds
            }));
            
            const expectApsi=[
                {
                    "CIS": 63825628,
                    "Name": "METASPIRINE, comprimé",
                    "score": 0.16666666666666666,
                    "type": "comprimé",
                },
                {
                    "CIS": 68799614,
                    "Name": "ASPIRINE DU RHÔNE 500 mg, comprimé",
                    "score": 0.11764705882352941,
                    "type": "comprimé",
                },
                {
                    "CIS": 65265765,
                    "Name": "ASPIRINE UPSA 500 mg, comprimé effervescent",
                    "score": 0.09302325581395349,
                    "type": "comprimé effervescent(e)",
                },
                {
                    "CIS": 69029253,
                    "Name": "ASPIRINE DU RHONE 500 mg, comprimé à croquer",
                    "score": 0.09090909090909091,
                    "type": "comprimé à croquer",
                },
                {
                    "CIS": 69781373,
                    "Name": "ASPIRINE pH 8 500 mg, comprimé gastro-résistant",
                    "score": 0.0851063829787234,
                    "type": "comprimé gastro-résistant(e)",
                },
                {
                    "CIS": 61946403,
                    "Name": "ASPIRINE ARROW 100 mg, comprimé gastro-résistant",
                    "score": 0.08333333333333333,
                    "type": "comprimé gastro-résistant(e)",
                },
                {
                    "CIS": 61464022,
                    "Name": "ASPIRINE PROTECT 100 mg, comprimé gastro-résistant",
                    "score": 0.08,
                    "type": "comprimé gastro-résistant(e)",
                },
                {
                    "CIS": 64872883,
                    "Name": "ASPIRINE PROTECT 300 mg, comprimé gastro-résistant",
                    "score": 0.08,
                    "type": "comprimé gastro-résistant(e)",
                },
                {
                    "CIS": 64849094,
                    "Name": "NOVACETOL (ASPIRINE PARACETAMOL), comprimé",
                    "score": 0.07547169811320754,
                    "type": "comprimé",
                },
                {
                    "CIS": 62358794,
                    "Name": "ASPIRINE 500 mg VITAMINE C OBERLIN, comprimé effervescent",
                    "score": 0.07017543859649122,
                    "type": "comprimé effervescent(e)",
                },
                {
                    "CIS": 61137191,
                    "Name": "ANTIGRIPPINE A L'ASPIRINE ETAT GRIPPAL, comprimé",
                    "score": 0.06153846153846154,
                    "type": "comprimé",
                },
                {
                    "CIS": 61172160,
                    "Name": "ASPIRINE UPSA TAMPONNEE EFFERVESCENTE 1000 mg, comprimé effervescent",
                    "score": 0.058823529411764705,
                    "type": "comprimé effervescent(e)",
                },
                {
                    "CIS": 67831952,
                    "Name": "ASPIRINE UPSA VITAMINEE C TAMPONNEE EFFERVESCENTE, comprimé effervescent",
                    "score": 0.05555555555555555,
                    "type": "comprimé effervescent(e)",
                },
                {
                    "CIS": 65057344,
                    "Name": "ASPIDIUM FILIX MAS BOIRON, degré de dilution compris entre 4CH et 30CH ou entre 7DH et 60DH",
                    "score": 0.04395604395604396,
                    "type": " comprimé et solution(s) et granules et poudre et pommade",
                }
            ]
        const searchString = 'Aspi';
        const result = searchMed(searchString);
        expect(result).toEqual(expectApsi);
        });
    });

    // describe('trouverNomMedicament', () => {
    //     it('should identify medication names within a text', () => {
    //         const text = "ordonance de 3 cachets Aspirin";
    //         const result = trouverNomMedicament(text);
    //         expect(result).toContain('Aspirin');
    //     });
    // });
});
