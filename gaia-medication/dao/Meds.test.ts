// Meds.test.js

import { getAllMed, getMedbyCIS, getAllGenOfCIS, getAllSameCompOfCIS, getAllPA, getComposition, getPAfromMed } from './Meds'; // Adjust the import path according to your project structure

describe('Meds Module Tests', () => {
  describe('getAllMed function', () => {
    it('should return an array of medications', () => {
      const meds = getAllMed();
      expect(Array.isArray(meds)).toBeTruthy();
      expect(meds.length).toBeGreaterThan(0);
    });
  });

  describe('getMedbyCIS function', () => {
    it('should return a medication for a valid CIS code', () => {
      const CIS = 64891296;
      const med = getMedbyCIS(CIS);
      expect(med).toBeDefined();
      expect(med.CIS).toEqual(CIS);
    });

    it('should return null for an invalid CIS code', () => {
      const med = getMedbyCIS('invalidCISCode');
      expect(med).toBeNull();
    });
  });

  describe('getAllGenOfCIS function', () => {
    it('should return an array of generic medications for a given CIS code', () => {
      const CIS = 64891296;
      const gens = getAllGenOfCIS(CIS);
      expect(Array.isArray(gens)).toBeTruthy();
      // Add more assertions as necessary
    });
  });

  describe('getAllSameCompOfCIS function', () => {
    it('should return an array of medications with the same composition for a given CIS code', () => {
      const CIS = 64891296;
      const comps = getAllSameCompOfCIS(CIS);
      expect(Array.isArray(comps)).toBeTruthy();
      // Add more assertions as necessary
    });
  });

  describe('getAllPA function', () => {
    it('should return a set of all unique active principles', () => {
      const allPA = getAllPA();
      expect(allPA).toBeInstanceOf(Set);
      expect(allPA.size).toBeGreaterThan(0);
    });
  });
  
  describe('getPAfromMed function', () => {
    it('should return a set of unique active principles for a given CIS code', () => {
      const CIS = 64891296; 
      const PAfromMed = getPAfromMed(CIS);
      expect(PAfromMed).toBeInstanceOf(Set);
      // If possible, check for a known active principle in the set
      // expect(PAfromMed.has('knownActivePrinciple')).toBeTruthy();
    });
  });
  
  describe('getComposition function', () => {
    it('should return a dictionary of types and their corresponding compositions', () => {
      const composition = [
        {
          "Principe actif": ["KnownActivePrinciple"],
          "Dosage": ["SomeDosage"],
          "Quantité": ["SomeQuantity"],
          "type": ["SomeType"]
        }
      ]; // Replace with actual value if needed
      const compositionDict = getComposition(composition);
      expect(typeof compositionDict).toBe('object');
      // Add more specific tests based on the expected structure
      // expect(compositionDict['SomeType']).toBeDefined();
    });
  });

  // Add more tests as needed for specific edge cases and error handling
});
