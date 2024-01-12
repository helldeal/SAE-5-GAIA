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
      
        // Add more test cases for different scenarios, such as AsyncStorage errors
      });

      describe('readList', () => {
        // Reset mocks before each test
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
      
        // Add more tests as needed
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
      
        // Add more tests as needed for error cases or different scenarios
      });


      describe('addItemToList', () => {
        beforeEach(() => {
          jest.clearAllMocks();
        });
      
        it('adds an item to an empty list', async () => {
          const key = 'testList';
          const newItem = { id: 1, name: 'New Item' };
      
          // Simulate an empty list in storage
          (AsyncStorage.getItem as jest.Mock).mockResolvedValue(null);
      
          await addItemToList(key, newItem);
      
          // Check that setItem was called with the correct arguments
          expect(AsyncStorage.setItem).toHaveBeenCalledWith(key, JSON.stringify([newItem]));
        });
      
        it('adds an item to an existing list', async () => {
          const key = 'testList';
          const existingItems = [{ id: 1, name: 'Existing Item' }];
          const newItem = { id: 2, name: 'New Item' };
      
          // Simulate an existing list in storage
          (AsyncStorage.getItem as jest.Mock).mockResolvedValue(JSON.stringify(existingItems));
      
          await addItemToList(key, newItem);
      
          // Check that setItem was called with the correct arguments
          expect(AsyncStorage.setItem).toHaveBeenCalledWith(key, JSON.stringify([...existingItems, newItem]));
        });
      
        // Add more tests as needed for error cases or different scenarios
      });


      describe('updateItemInList', () => {
        beforeEach(() => {
          jest.clearAllMocks();
        });
      
        it('updates an item in the list', async () => {
          const key = 'testList';
          const existingList = [{ id: 1, name: 'Item1' }, { id: 2, name: 'Item2' }];
          const updatedItem = { id: 1, name: 'Updated Item' };
      
          // Simulate existing list in storage
          (AsyncStorage.getItem as jest.Mock).mockResolvedValue(JSON.stringify(existingList));
      
          await updateItemInList(key, 0, updatedItem);
      
          // Check that setItem was called with the correct arguments
          expect(AsyncStorage.setItem).toHaveBeenCalledWith(key, JSON.stringify([updatedItem, existingList[1]]));
        });
      
        it('does not update for an invalid index', async () => {
          const key = 'testList';
          const existingList = [{ id: 1, name: 'Item1' }];
          const newItem = { id: 2, name: 'New Item' };
      
          // Simulate existing list in storage
          (AsyncStorage.getItem as jest.Mock).mockResolvedValue(JSON.stringify(existingList));
      
          await updateItemInList(key, 2, newItem);
      
          // Check that setItem was not called since the index is invalid
          expect(AsyncStorage.setItem).not.toHaveBeenCalled();
        });
      
        // Add more tests as needed for error cases or different scenarios
      });



      describe('removeItemFromList', () => {
        beforeEach(() => {
          jest.clearAllMocks();
        });
      
        it('removes an item from the list', async () => {
          const key = 'testList';
          const existingList = [{ id: 1, name: 'Item1' }, { id: 2, name: 'Item2' }];
      
          // Simulate existing list in storage
          (AsyncStorage.getItem as jest.Mock).mockResolvedValue(JSON.stringify(existingList));
      
          await removeItemFromList(key, 0);
      
          // Check that setItem was called with the correct arguments
          expect(AsyncStorage.setItem).toHaveBeenCalledWith(key, JSON.stringify([existingList[1]]));
        });
      
        it('does not remove an item for an invalid index', async () => {
          const key = 'testList';
          const existingList = [{ id: 1, name: 'Item1' }];
      
          // Simulate existing list in storage
          (AsyncStorage.getItem as jest.Mock).mockResolvedValue(JSON.stringify(existingList));
      
          await removeItemFromList(key, 2);
      
          // Check that setItem was not called since the index is invalid
          expect(AsyncStorage.setItem).not.toHaveBeenCalled();
        });
      
        // Add more tests as needed for error cases or different scenarios
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
      
          // Simulate existing list in storage
          (AsyncStorage.getItem as jest.Mock).mockResolvedValue(JSON.stringify(existingList));
      
          await removeItemFromStock(cisToRemove, cipToRemove, idUserToRemove);
      
          // Check that setItem was called with the correct arguments
          expect(AsyncStorage.setItem).toHaveBeenCalledWith(key, JSON.stringify([]));
        });
      
        it('does not remove an item if it does not exist', async () => {
          const key = 'stock';
          const existingList = [{ CIS: '123', CIP: '456', idUser: 1 }];
          const cisToRemove = '999';
          const cipToRemove = '888';
          const idUserToRemove = 2;
      
          // Simulate existing list in storage
          (AsyncStorage.getItem as jest.Mock).mockResolvedValue(JSON.stringify(existingList));
      
          await removeItemFromStock(cisToRemove, cipToRemove, idUserToRemove);
      
          // Check that setItem was not called since the item does not exist
          expect(AsyncStorage.setItem).not.toHaveBeenCalled();
        });
      
        // Add more tests as needed for error cases or different scenarios
      });

      describe('getAllTreatments', () => {
        beforeEach(() => {
          jest.clearAllMocks();
        });
      
        it('returns an empty array when there are no treatments', async () => {
          (AsyncStorage.getItem as jest.Mock).mockResolvedValue(null);
      
          const treatments = await getAllTreatments();
          expect(treatments).toEqual([]);
        });
      
        it('returns a list of treatments when they are present', async () => {
          const mockTreatments = JSON.stringify([
            // Add mock treatment objects here
            // Example: { name: 'Treatment1', userId: 1, ... }
          ]);
      
          (AsyncStorage.getItem as jest.Mock).mockResolvedValue(mockTreatments);
      
          const treatments = await getAllTreatments();
          // Add expectations to check if treatments are processed correctly
          // Example: expect(treatments).toEqual([...]);
        });
      
        // Add more tests as needed for error cases or different scenarios
      });
});