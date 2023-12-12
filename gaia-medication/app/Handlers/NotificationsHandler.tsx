import * as Notifications from 'expo-notifications';

//--------------------//

export const requestNotificationPermissions = async () => {
  const { status } = await Notifications.getPermissionsAsync();
  if (status !== 'granted') {
    const { status: newStatus } = await Notifications.requestPermissionsAsync();
    if (newStatus !== 'granted') {
      console.log('Notification permissions not granted');
      return false;
    }
  }
  return true;
};

export const scheduleLocalNotification = async (
    title: string, 
    subtitle: string, 
    body: string, 
    data = {}, 
    sound: string, 
    color: string, 
    priority: Notifications.AndroidNotificationPriority, 
    categoryIdentifier: string,
    date: Date,
  ) => {
  const notificationId = await Notifications.scheduleNotificationAsync({
    content: {
      title,
      subtitle,
      body,
      data,
      sound,
      color,
      priority,
      categoryIdentifier,
    },
    trigger: {
      hour: date.getHours(),
      minute: date.getMinutes(),
      repeats: true
    }
  });
  return notificationId;
};

//--------------------//

export const notificationDaily = async () => {
  let dateOfNotif = new Date()
  dateOfNotif.setSeconds(20)
  dateOfNotif.setMinutes(52)
  console.log(dateOfNotif)
  await scheduleLocalNotification(
    "🦠 Rappel ", 
    "Votre traitement", 
    "Aujourd'hui :\n\n 💊 Doliprane 700\n 💊 Aspirine\n 💊 Betadine", 
    { data: "data" }, 
    "default", 
    "default", 
    Notifications.AndroidNotificationPriority.DEFAULT,
    "reminder",
    dateOfNotif
  );
}

export const notificationNow = async () => {
  let dateOfNotif = new Date()
  dateOfNotif.setDate(12)
  dateOfNotif.setFullYear(2024)
  dateOfNotif.setHours(14)
  dateOfNotif.setMinutes(30)
  scheduleLocalNotification(
    "🦠 Rappel ", 
    "Votre traitement", 
    "C'est le moment ! : \n💊 Doliprane 700", 
    { data: "data" }, 
    "default", 
    "default", 
    Notifications.AndroidNotificationPriority.DEFAULT,
    "reminder",
    dateOfNotif
  );
}

export const notificationForgot = async () => {
  let dateOfNotif = new Date()
  dateOfNotif.setDate(12)
  dateOfNotif.setMonth(12)
  dateOfNotif.setFullYear(2023)
  dateOfNotif.setHours(14)
  dateOfNotif.setMinutes(32)
  scheduleLocalNotification(
    "⚠️ N'oubliez pas !", 
    "Votre traitement", 
    "Avez vous pensé à prendre votre : \n\n 💊 Doliprane 700 ?",
    { data: "data" }, 
    "default", 
    "red", 
    Notifications.AndroidNotificationPriority.HIGH,
    "alertReminder",
    dateOfNotif
  );
}

//--------------------//

Notifications.setNotificationCategoryAsync('reminder', [
  {
    identifier: 'take',
    buttonTitle: "Pris !",
    options: {
      isDestructive: false,
      isAuthenticationRequired: false,
    },
  },
  {
    identifier: 'snooze',
    buttonTitle: 'Rappeler dans 30 minutes',
    options: {
      isDestructive: false,
      isAuthenticationRequired: false,
    },
  },
]);

Notifications.setNotificationCategoryAsync('alertReminder', [
  {
    identifier: 'take',
    buttonTitle: 'Pris !',
    options: {
      isDestructive: false,
      isAuthenticationRequired: false,
    },
  },
  {
    identifier: 'snooze',
    buttonTitle: 'Rappeler dans 15 minutes',
    options: {
      isDestructive: false,
      isAuthenticationRequired: false,
    },
  },
]);

//--------------------//
