import{UserIdAutoIncrement,readList,getUserByID,addItemToList,updateItemInList,removeItemFromList,removeItemFromStock,getAllTreatments,initTreatments,getTreatmentByName,getDaysTakes,}from './Storage'
import AsyncStorage from "@react-native-async-storage/async-storage";
jest.mock('@react-native-async-storage/async-storage', () => ({
    setItem: jest.fn().mockResolvedValue(undefined),
    getItem: jest.fn().mockResolvedValue(null), // Default mock, can be overridden in tests
  }));
  
describe('Storage Module Tests', () => {

    describe('UserIdAutoIncrement', () => {
        it('should return the next available user ID', async () => {
          
          const mockUsers = [
            { id: 1, name: 'User1' },
            { id: 2, name: 'User2' },
            { id: 4, name: 'User4' },
          ];
          AsyncStorage.getItem = jest.fn().mockResolvedValue(JSON.stringify(mockUsers));
      
          const nextUserId = await UserIdAutoIncrement();
          expect(nextUserId).toBe(3);
        });
      
        it('should return 1 for empty storage', async () => {
          AsyncStorage.getItem = jest.fn().mockResolvedValue(null);
      
          const nextUserId = await UserIdAutoIncrement();
          expect(nextUserId).toBe(1);
        });
      });

      describe('readList', () => {
        beforeEach(() => {
          jest.clearAllMocks();
        });
      
        it('returns a parsed list when value exists', async () => {
          const testKey = 'testKey';
          const testData = ['item1', 'item2'];
          (AsyncStorage.getItem as jest.Mock).mockResolvedValue(JSON.stringify(testData));
      
          const result = await readList(testKey);
          expect(result).toEqual(testData);
        });
      
        it('returns an empty array when no item is found', async () => {
          const testKey = 'nonExistentKey';
          // Explicitly mock to return null for this key
          (AsyncStorage.getItem as jest.Mock).mockResolvedValue(null);
      
          const result = await readList(testKey);
          expect(result).toEqual([]);
        });
      });


      describe('getUserByID', () => {
        beforeEach(() => {
          jest.clearAllMocks();
        });
      
        it('returns a user when they exist', async () => {
          const users = [{ id: 1, name: 'John Doe' }, { id: 2, name: 'Jane Doe' }];
          (AsyncStorage.getItem as jest.Mock).mockResolvedValue(JSON.stringify(users));
      
          const user = await getUserByID(1);
          expect(user).toEqual({ id: 1, name: 'John Doe' });
        });
      
        it('returns null when the user does not exist', async () => {
          const users = [{ id: 1, name: 'John Doe' }];
          (AsyncStorage.getItem as jest.Mock).mockResolvedValue(JSON.stringify(users));
      
          const user = await getUserByID(2);
          expect(user).toBeNull();
        });
      
        it('returns null when there are no users', async () => {
          (AsyncStorage.getItem as jest.Mock).mockResolvedValue(null);
      
          const user = await getUserByID(1);
          expect(user).toBeNull();
        });
      });


      describe('addItemToList', () => {
        beforeEach(() => {
          jest.clearAllMocks();
        });
      
        it('adds an item to an empty list', async () => {
          const key = 'testList';
          const newItem = { id: 1, name: 'New Item' };
      
          (AsyncStorage.getItem as jest.Mock).mockResolvedValue(null);
      
          await addItemToList(key, newItem);
      
          expect(AsyncStorage.setItem).toHaveBeenCalledWith(key, JSON.stringify([newItem]));
        });
      
        it('adds an item to an existing list', async () => {
          const key = 'testList';
          const existingItems = [{ id: 1, name: 'Existing Item' }];
          const newItem = { id: 2, name: 'New Item' };
      
          (AsyncStorage.getItem as jest.Mock).mockResolvedValue(JSON.stringify(existingItems));
      
          await addItemToList(key, newItem);
      
          expect(AsyncStorage.setItem).toHaveBeenCalledWith(key, JSON.stringify([...existingItems, newItem]));
        });
      
      });


      describe('updateItemInList', () => {
        beforeEach(() => {
          jest.clearAllMocks();
        });
      
        it('updates an item in the list', async () => {
          const key = 'testList';
          const existingList = [{ id: 1, name: 'Item1' }, { id: 2, name: 'Item2' }];
          const updatedItem = { id: 1, name: 'Updated Item' };
      
          (AsyncStorage.getItem as jest.Mock).mockResolvedValue(JSON.stringify(existingList));
      
          await updateItemInList(key, 0, updatedItem);
      
          expect(AsyncStorage.setItem).toHaveBeenCalledWith(key, JSON.stringify([updatedItem, existingList[1]]));
        });
      
        it('does not update for an invalid index', async () => {
          const key = 'testList';
          const existingList = [{ id: 1, name: 'Item1' }];
          const newItem = { id: 2, name: 'New Item' };
      
          (AsyncStorage.getItem as jest.Mock).mockResolvedValue(JSON.stringify(existingList));
      
          await updateItemInList(key, 2, newItem);
      
          expect(AsyncStorage.setItem).not.toHaveBeenCalled();
        });
      });



      describe('removeItemFromList', () => {
        beforeEach(() => {
          jest.clearAllMocks();
        });
      
        it('removes an item from the list', async () => {
          const key = 'testList';
          const existingList = [{ id: 1, name: 'Item1' }, { id: 2, name: 'Item2' }];
      
          (AsyncStorage.getItem as jest.Mock).mockResolvedValue(JSON.stringify(existingList));
      
          await removeItemFromList(key, 0);
      
          expect(AsyncStorage.setItem).toHaveBeenCalledWith(key, JSON.stringify([existingList[1]]));
        });
      
        it('does not remove an item for an invalid index', async () => {
          const key = 'testList';
          const existingList = [{ id: 1, name: 'Item1' }];
      
          (AsyncStorage.getItem as jest.Mock).mockResolvedValue(JSON.stringify(existingList));
      
          await removeItemFromList(key, 2);
      
          expect(AsyncStorage.setItem).not.toHaveBeenCalled();
        });
      });


      describe('removeItemFromStock', () => {
        beforeEach(() => {
          jest.clearAllMocks();
        });
      
        it('removes an item from the stock', async () => {
          const key = 'stock';
          const existingList = [{ CIS: '123', CIP: '456', idUser: 1 }];
          const cisToRemove = '123';
          const cipToRemove = '456';
          const idUserToRemove = 1;
      
          (AsyncStorage.getItem as jest.Mock).mockResolvedValue(JSON.stringify(existingList));
      
          await removeItemFromStock(cisToRemove, cipToRemove, idUserToRemove);
      
          expect(AsyncStorage.setItem).toHaveBeenCalledWith(key, JSON.stringify([]));
        });
      
        it('does not remove an item if it does not exist', async () => {
          const existingList = [{ CIS: '123', CIP: '456', idUser: 1 }];
          const cisToRemove = '999';
          const cipToRemove = '888';
          const idUserToRemove = 2;
      
          (AsyncStorage.getItem as jest.Mock).mockResolvedValue(JSON.stringify(existingList));
      
          await removeItemFromStock(cisToRemove, cipToRemove, idUserToRemove);
      
          expect(AsyncStorage.setItem).not.toHaveBeenCalled();
        });
      });

      
});

// jest.clearAllMocks();
// jest.mock('./Storage', () => ({
//     ...jest.requireActual('./Storage'), // keep the other exports of the module unchanged
//     getAllTreatments: jest.fn(), // mock only getAllTreatments
//   }));
  
//   const mockTreatments = [
//     {
//         description: 'Description1',
//         instructions: [
//             {
//                 CIS: 63283736,
//                 endDate: null,
//                 endModality: "number",
//                 endQuantity: 10,
//                 name: "Med1",
//                 quantity: 2,
//                 regularFrequency: true,
//                 regularFrequencyContinuity: "daily",
//                 regularFrequencyDays: null,
//                 regularFrequencyMode: "regular",
//                 regularFrequencyNumber: "1",
//                 regularFrequencyPeriods: "day",
//                 takes: [
//                     {
//                         CIS: 63283736,
//                         date: "2024-01-10T09:30:00.000Z",
//                         quantity: 0,
//                         taken: true,
//                         treatmentName: "TraitementTest1",
//                         userId: 1,
//                         review: "c'est pas bon"
//                     },
//                     {
//                         CIS: 63283736,
//                         date: "2024-01-10T15:23:00.000Z",
//                         quantity: 0,
//                         taken: true,
//                         treatmentName: "TraitementTest1",
//                         userId: 1,
//                         review: "Je suis mort avec ce truc"
//                     }
//                 ] 
//             },
//         ],                
//         name: 'Treatment1',
//         startDate: new Date("2024-01-10T13:44:03.404Z"),
//         userId: 1
//     },
//     {
//         description: 'Description2',
//         instructions: [
//             {
//                 CIS: 63283737,
//                 endDate: null,
//                 endModality: "number",
//                 endQuantity: 10,
//                 name: "Med2",
//                 quantity: 2,
//                 regularFrequency: true,
//                 regularFrequencyContinuity: "daily",
//                 regularFrequencyDays: null,
//                 regularFrequencyMode: "regular",
//                 regularFrequencyNumber: "2",
//                 regularFrequencyPeriods: "day",
//                 takes: [
//                     {
//                         CIS: 63283737,
//                         date: "2024-01-10T09:30:00.000Z",
//                         quantity: 0,
//                         taken: true,
//                         treatmentName: "TraitementTest2",
//                         userId: 1,
//                         review: "c'est super cool"
//                     },
//                     {
//                         CIS: 63283737,
//                         date: "2024-01-10T15:23:00.000Z",
//                         quantity: 0,
//                         taken: true,
//                         treatmentName: "TraitementTest2",
//                         userId: 1,
//                         review: "Pas si cool que ca enfait"
//                     }
//                 ] 
//             },
//         ],                
//         name: 'Treatment2',
//         startDate: new Date("2024-01-10T13:44:03.404Z"),
//         userId: 1
//     },
//   ];
//   const mockTakes = [
//     {
//         med: "Med1",
//         take: {
//             CIS: 63283736,
//             date: "2024-01-10T09:30:00.000Z",
//             quantity: 0,
//             taken: true,
//             treatmentName: "TraitementTest1",
//             userId: 1,
//             review: "c'est pas bon"
//         },
//         treatmentDescription: "Description1",
//         treatmentName: "Treatment1",
//     },
//     {
//         med: "Med1",
//         take: {
//             CIS: 63283736,
//             date: "2024-01-10T15:23:00.000Z",
//             quantity: 0,
//             taken: true,
//             treatmentName: "TraitementTest1",
//             userId: 1,
//             review: "Je suis mort avec ce truc"
//         },
//         treatmentDescription: "Description1",
//         treatmentName: "Treatment1",
//     },
//     {
//         med: "Med2",
//         take: {
//             CIS: 63283737,
//             date: "2024-01-10T09:30:00.000Z",
//             quantity: 0,
//             taken: true,
//             treatmentName: "TraitementTest2",
//             userId: 1,
//             review: "c'est super cool"
//         },
//         treatmentDescription: "Description2",
//         treatmentName: "Treatment2",
//     },
//     {
//         med: "Med2",
//         take: {
//             CIS: 63283737,
//             date: "2024-01-10T15:23:00.000Z",
//             quantity: 0,
//             taken: true,
//             treatmentName: "TraitementTest2",
//             userId: 1,
//             review: "Pas si cool que ca enfait"
//         },
//         treatmentDescription: "Description2",
//         treatmentName: "Treatment2",
//     },];


//   describe('initTreatments', () => {
//     it('returns an array of takes based on treatments', async () => {
//       (getAllTreatments as jest.Mock).mockResolvedValue(mockTreatments);
//       const takes = await initTreatments();
//       expect(takes).toEqual(mockTakes);
//     });
//   });

//   describe('getTreatmentByName', () => {
//     it('returns a treatment when it exists', async () => {
//       (getAllTreatments as jest.Mock).mockResolvedValue(mockTreatments);
//       const treatment = await getTreatmentByName('Treatment1',1);
//       expect(treatment).toEqual(mockTreatments[0]);
//     });

//     it('returns null when the treatment does not exist', async () => {
//       (getAllTreatments as jest.Mock).mockResolvedValue(mockTreatments);
//       const treatment = await getTreatmentByName('Treatment3',1);
//       expect(treatment).toBeNull();
//     });
//   });