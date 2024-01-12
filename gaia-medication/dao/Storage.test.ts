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
});