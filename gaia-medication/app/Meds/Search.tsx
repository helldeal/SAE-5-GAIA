import { useIsFocused } from '@react-navigation/native';
import React, { useEffect } from 'react';
import { View, Text, Button } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { searchMed } from '../../dao/Search';

export default function SearchPage() {
  const isFocused = useIsFocused();
  useEffect(() => {
    if(isFocused){ 
      console.log("Nav on Search Page")
    }
  },[isFocused]); 
  
  //searchMed(text)
  return (
    <View>
      <Text>Search</Text>
    </View>
  );
}