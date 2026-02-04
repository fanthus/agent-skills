---
name: react-native-app
description: Build cross-platform mobile applications using React Native. Use when the user wants to create, develop, or work with React Native apps for iOS and Android. Triggers include requests to build mobile apps, create React Native components, set up navigation, integrate native modules, handle app state management, implement animations, or work with React Native specific features like FlatList, StyleSheet, or platform-specific code.
---

# React Native App Development

## Overview

Create professional cross-platform mobile applications using React Native. This skill provides production-ready patterns, best practices, and utilities for building iOS and Android apps with a single codebase.

## Core Project Structure

Always organize React Native projects with this proven structure:

```
my-app/
├── src/
│   ├── components/       # Reusable UI components
│   ├── screens/          # Screen-level components
│   ├── navigation/       # Navigation setup
│   ├── services/         # API calls, storage, etc.
│   ├── hooks/            # Custom React hooks
│   ├── utils/            # Helper functions
│   ├── constants/        # Colors, sizes, config
│   ├── types/            # TypeScript types
│   └── App.tsx           # Root component
├── android/              # Native Android code
├── ios/                  # Native iOS code
├── assets/               # Images, fonts, etc.
└── package.json
```

## Quick Start Patterns

### Basic Screen Component

```typescript
import React from 'react';
import { View, Text, StyleSheet, SafeAreaView } from 'react-native';

export const HomeScreen = () => {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>Welcome</Text>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  content: {
    flex: 1,
    padding: 16,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
  },
});
```

### React Navigation Setup

```typescript
// navigation/AppNavigator.tsx
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Stack = createNativeStackNavigator();

export const AppNavigator = () => (
  <NavigationContainer>
    <Stack.Navigator>
      <Stack.Screen name="Home" component={HomeScreen} />
      <Stack.Screen name="Details" component={DetailsScreen} />
    </Stack.Navigator>
  </NavigationContainer>
);
```

### Tab Navigation

```typescript
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Icon from 'react-native-vector-icons/Ionicons';

const Tab = createBottomTabNavigator();

export const TabNavigator = () => (
  <Tab.Navigator>
    <Tab.Screen 
      name="Home" 
      component={HomeScreen}
      options={{
        tabBarIcon: ({ color, size }) => (
          <Icon name="home" size={size} color={color} />
        ),
      }}
    />
  </Tab.Navigator>
);
```

## Essential Patterns

### FlatList with Optimization

```typescript
<FlatList
  data={items}
  renderItem={({ item }) => <ItemCard item={item} />}
  keyExtractor={item => item.id}
  // Performance optimizations
  removeClippedSubviews={true}
  maxToRenderPerBatch={10}
  updateCellsBatchingPeriod={50}
  windowSize={21}
  // Pull to refresh
  onRefresh={handleRefresh}
  refreshing={isRefreshing}
  // Empty state
  ListEmptyComponent={<EmptyState />}
/>
```

### Custom Hooks

```typescript
// hooks/useAsync.ts
export const useAsync = <T,>(asyncFn: () => Promise<T>) => {
  const [state, setState] = useState({
    loading: true,
    data: null as T | null,
    error: null as Error | null,
  });

  useEffect(() => {
    asyncFn()
      .then(data => setState({ loading: false, data, error: null }))
      .catch(error => setState({ loading: false, data: null, error }));
  }, []);

  return state;
};
```

### Responsive Styles

```typescript
import { Dimensions, Platform } from 'react-native';

const { width, height } = Dimensions.get('window');

const styles = StyleSheet.create({
  container: {
    padding: width > 600 ? 32 : 16, // Tablet vs phone
  },
  text: {
    fontSize: Platform.select({ ios: 16, android: 14 }),
  },
});
```

### Animated Components

```typescript
import Animated, { 
  useAnimatedStyle, 
  withSpring,
  useSharedValue 
} from 'react-native-reanimated';

const MyComponent = () => {
  const offset = useSharedValue(0);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ translateX: withSpring(offset.value) }],
  }));

  return <Animated.View style={animatedStyle} />;
};
```

## State Management

### Context API Pattern

```typescript
// contexts/AuthContext.tsx
interface AuthContextType {
  user: User | null;
  login: (credentials: Credentials) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType>(null!);

export const AuthProvider: React.FC<{children: React.ReactNode}> = ({children}) => {
  const [user, setUser] = useState<User | null>(null);

  const login = async (credentials: Credentials) => {
    const user = await authService.login(credentials);
    setUser(user);
  };

  const logout = () => setUser(null);

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
```

### Redux Toolkit Integration

```typescript
import { configureStore, createSlice } from '@reduxjs/toolkit';

const userSlice = createSlice({
  name: 'user',
  initialState: { profile: null },
  reducers: {
    setProfile: (state, action) => {
      state.profile = action.payload;
    },
  },
});

export const store = configureStore({
  reducer: {
    user: userSlice.reducer,
  },
});
```

## Platform-Specific Code

### Conditional Rendering

```typescript
import { Platform } from 'react-native';

const Component = () => (
  <>
    {Platform.OS === 'ios' && <IOSComponent />}
    {Platform.OS === 'android' && <AndroidComponent />}
  </>
);
```

### File Extensions

Create platform-specific files:
- `Component.ios.tsx` - iOS only
- `Component.android.tsx` - Android only
- `Component.tsx` - Shared fallback

## Performance Best Practices

### Memoization

```typescript
const Item = React.memo(({ item }) => (
  <View><Text>{item.name}</Text></View>
));

const computedValue = useMemo(() => 
  expensiveCalculation(data), 
  [data]
);

const handlePress = useCallback(() => {
  doSomething(id);
}, [id]);
```

### Image Optimization

```typescript
<Image 
  source={{ uri: imageUrl }}
  style={styles.image}
  resizeMode="cover"
  // Cache control
  defaultSource={require('../assets/placeholder.png')}
/>
```

## Native Module Integration

### Linking Native Libraries

```bash
# Auto-linking (RN 0.60+)
npm install react-native-library
cd ios && pod install

# Manual linking (older versions)
react-native link react-native-library
```

### Permissions Handling

```typescript
import { PermissionsAndroid, Platform } from 'react-native';

const requestCameraPermission = async () => {
  if (Platform.OS === 'android') {
    const granted = await PermissionsAndroid.request(
      PermissionsAndroid.PERMISSIONS.CAMERA
    );
    return granted === PermissionsAndroid.RESULTS.GRANTED;
  }
  return true; // iOS handles via Info.plist
};
```

## Common Utilities

### Storage Helper

```typescript
import AsyncStorage from '@react-native-async-storage/async-storage';

export const storage = {
  get: async (key: string) => {
    const value = await AsyncStorage.getItem(key);
    return value ? JSON.parse(value) : null;
  },
  set: async (key: string, value: any) => {
    await AsyncStorage.setItem(key, JSON.stringify(value));
  },
  remove: async (key: string) => {
    await AsyncStorage.removeItem(key);
  },
};
```

### API Service

```typescript
// services/api.ts
const API_BASE = 'https://api.example.com';

export const api = {
  get: async <T>(endpoint: string): Promise<T> => {
    const response = await fetch(`${API_BASE}${endpoint}`);
    if (!response.ok) throw new Error('Request failed');
    return response.json();
  },
  post: async <T>(endpoint: string, data: any): Promise<T> => {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response.json();
  },
};
```

## Debugging Tips

### React Native Debugger

```typescript
// Enable in development
if (__DEV__) {
  console.log('Development mode');
  // Access dev menu: Cmd+D (iOS) or Cmd+M (Android)
}
```

### Performance Monitoring

```typescript
import { InteractionManager } from 'react-native';

InteractionManager.runAfterInteractions(() => {
  // Expensive task after animations complete
});
```

## TypeScript Integration

### Navigation Types

```typescript
type RootStackParamList = {
  Home: undefined;
  Profile: { userId: string };
  Settings: undefined;
};

type HomeScreenProps = NativeStackScreenProps<RootStackParamList, 'Home'>;
```

### Component Props

```typescript
interface ButtonProps {
  title: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}

const Button: React.FC<ButtonProps> = ({ title, onPress, variant = 'primary', disabled }) => {
  // Component implementation
};
```

## Testing Considerations

When building React Native apps, structure code to be testable:
- Extract business logic into pure functions
- Use dependency injection for services
- Keep components simple and presentational
- Test navigation separately from component logic

## Build Configuration

### Environment Variables

```typescript
// config/env.ts
export const config = {
  API_URL: __DEV__ 
    ? 'http://localhost:3000' 
    : 'https://api.production.com',
  FEATURE_FLAGS: {
    newUI: true,
  },
};
```

## Additional Resources

For detailed component patterns, styling guidelines, and advanced topics, see the reference files in the `references/` directory:
- `component-patterns.md` - Detailed component patterns and examples
- `styling-guide.md` - Comprehensive styling best practices
- `performance.md` - Advanced optimization techniques
