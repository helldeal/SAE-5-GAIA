import React, { useEffect } from "react";
import { View, Text, StatusBar,  } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useRouter, useFocusEffect } from 'expo-router';
import { Redirect } from 'expo-router';



const Login = () => { 

  return (
    <SafeAreaView edges={['top']}>
      <StatusBar backgroundColor="blue" />
      <Text>LOGIN</Text>
    </SafeAreaView>
  );
}

export default Login;
