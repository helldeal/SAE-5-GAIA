import { StyleSheet, Text, View, StatusBar } from 'react-native';
import Home from './app/Home/Home';
import Navigation from './app/Navigation';
import { SafeAreaView } from 'react-native-safe-area-context';



export default function App() {
  return (
    <View style={styles.container}>
      <StatusBar barStyle={"dark-content"} backgroundColor="transparent" />
      <Navigation />
    </View> 
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
    //alignItems: 'center',
   // justifyContent: 'center',
  },
});

