# React Native Performance Optimization

## Rendering Optimization

### React.memo for Functional Components

```typescript
const ExpensiveComponent = React.memo(({ data }) => {
  // This will only re-render if data changes
  return <View>{/* Complex rendering */}</View>;
}, (prevProps, nextProps) => {
  // Custom comparison function (optional)
  return prevProps.data.id === nextProps.data.id;
});
```

### useMemo for Expensive Calculations

```typescript
const ProcessedData = () => {
  const data = useSelector(state => state.data);
  
  const processedData = useMemo(() => {
    // Expensive operation
    return data.map(item => ({
      ...item,
      computed: heavyCalculation(item),
    }));
  }, [data]); // Only recalculate when data changes

  return <DataList data={processedData} />;
};
```

### useCallback for Function Props

```typescript
const ParentComponent = () => {
  const [count, setCount] = useState(0);
  
  // Without useCallback, this creates a new function on every render
  const handlePress = useCallback(() => {
    console.log('Pressed', count);
  }, [count]);
  
  return <ChildComponent onPress={handlePress} />;
};

const ChildComponent = React.memo(({ onPress }) => {
  return <Button onPress={onPress} />;
});
```

## FlatList Optimization

### Essential Performance Props

```typescript
<FlatList
  data={items}
  renderItem={renderItem}
  keyExtractor={item => item.id}
  
  // Performance optimizations
  removeClippedSubviews={true} // Unmount far offscreen items
  maxToRenderPerBatch={10} // Render items in batches
  updateCellsBatchingPeriod={50} // Delay between batches (ms)
  initialNumToRender={10} // Items to render initially
  windowSize={21} // Items in memory (pages)
  
  // Item height optimization
  getItemLayout={(data, index) => ({
    length: ITEM_HEIGHT,
    offset: ITEM_HEIGHT * index,
    index,
  })}
/>
```

### Optimize renderItem

```typescript
// Bad: Creates new component on every render
const renderItem = ({ item }) => <ItemCard item={item} />;

// Good: Memoized component
const ItemCard = React.memo(({ item }) => (
  <View><Text>{item.name}</Text></View>
));

const renderItem = useCallback(({ item }) => (
  <ItemCard item={item} />
), []);
```

### Optimize Key Extraction

```typescript
// Bad: Creates new function every render
keyExtractor={item => item.id.toString()}

// Good: Separate stable function
const keyExtractor = (item) => item.id;

<FlatList keyExtractor={keyExtractor} />
```

## Image Optimization

### Proper Image Sizing

```typescript
<Image
  source={{ uri: imageUrl }}
  style={{ width: 300, height: 200 }}
  resizeMode="cover"
  // Cache optimization
  defaultSource={require('./placeholder.png')}
/>
```

### Use FastImage Library

```typescript
import FastImage from 'react-native-fast-image';

<FastImage
  style={styles.image}
  source={{
    uri: imageUrl,
    priority: FastImage.priority.normal,
    cache: FastImage.cacheControl.immutable,
  }}
  resizeMode={FastImage.resizeMode.cover}
/>
```

### Progressive Image Loading

```typescript
const ProgressiveImage = ({ source, style }) => {
  const [loading, setLoading] = useState(true);
  const thumbnailAnimated = useRef(new Animated.Value(0)).current;
  const imageAnimated = useRef(new Animated.Value(0)).current;

  const handleThumbnailLoad = () => {
    Animated.timing(thumbnailAnimated, {
      toValue: 1,
      useNativeDriver: true,
    }).start();
  };

  const onImageLoad = () => {
    setLoading(false);
    Animated.timing(imageAnimated, {
      toValue: 1,
      useNativeDriver: true,
    }).start();
  };

  return (
    <View style={style}>
      <Animated.Image
        source={source.thumbnail}
        style={[style, { opacity: thumbnailAnimated }]}
        onLoad={handleThumbnailLoad}
        blurRadius={1}
      />
      <Animated.Image
        source={source.full}
        style={[style, { opacity: imageAnimated }, styles.imageOverlay]}
        onLoad={onImageLoad}
      />
    </View>
  );
};
```

## Navigation Optimization

### Lazy Screen Loading

```typescript
import React, { lazy, Suspense } from 'react';

const LazyScreen = lazy(() => import('./HeavyScreen'));

const Stack.Screen 
  name="Heavy"
  component={() => (
    <Suspense fallback={<LoadingScreen />}>
      <LazyScreen />
    </Suspense>
  )}
/>
```

### Avoid Inline Navigation Options

```typescript
// Bad
<Stack.Screen 
  name="Home"
  component={HomeScreen}
  options={{ headerTitle: 'Home' }} // Creates new object every render
/>

// Good
const screenOptions = { headerTitle: 'Home' };
<Stack.Screen 
  name="Home"
  component={HomeScreen}
  options={screenOptions}
/>
```

## Animation Performance

### Use Native Driver

```typescript
// Always enable useNativeDriver when possible
Animated.timing(animatedValue, {
  toValue: 100,
  duration: 300,
  useNativeDriver: true, // Runs on native thread
}).start();

// Works for: transform, opacity
// Does NOT work for: layout properties (width, height, etc.)
```

### Use Reanimated for Complex Animations

```typescript
import Animated, {
  useAnimatedStyle,
  useSharedValue,
  withSpring,
} from 'react-native-reanimated';

const AnimatedComponent = () => {
  const offset = useSharedValue(0);

  const animatedStyles = useAnimatedStyle(() => ({
    transform: [{ translateX: withSpring(offset.value) }],
  }));

  return <Animated.View style={animatedStyles} />;
};
```

### LayoutAnimation for Simple Transitions

```typescript
import { LayoutAnimation, UIManager, Platform } from 'react-native';

if (Platform.OS === 'android') {
  UIManager.setLayoutAnimationEnabledExperimental?.(true);
}

const handlePress = () => {
  LayoutAnimation.configureNext(LayoutAnimation.Presets.easeInEaseOut);
  setExpanded(!expanded);
};
```

## State Management Optimization

### Avoid Unnecessary Context Re-renders

```typescript
// Bad: Everything re-renders when anything changes
const AppContext = createContext({ user, theme, settings });

// Good: Split contexts by update frequency
const UserContext = createContext(user);
const ThemeContext = createContext(theme);
const SettingsContext = createContext(settings);
```

### Selector Optimization with Redux

```typescript
import { createSelector } from 'reselect';

// Memoized selector
const selectVisibleItems = createSelector(
  state => state.items,
  state => state.filter,
  (items, filter) => items.filter(item => item.category === filter)
);

// Use in component
const visibleItems = useSelector(selectVisibleItems);
```

## InteractionManager for Heavy Tasks

```typescript
import { InteractionManager } from 'react-native';

useEffect(() => {
  // Wait for all interactions/animations to complete
  const task = InteractionManager.runAfterInteractions(() => {
    // Heavy computation or data fetching
    processLargeDataset();
  });

  return () => task.cancel();
}, []);
```

## Bundle Size Optimization

### Code Splitting

```typescript
// Import only what you need
import { pick } from 'lodash'; // ❌ Imports entire library
import pick from 'lodash/pick'; // ✅ Imports only pick

// Use babel-plugin-lodash
import { pick } from 'lodash'; // With plugin, this is optimized
```

### Remove Console Logs in Production

```javascript
// babel.config.js
module.exports = {
  presets: ['module:metro-react-native-babel-preset'],
  env: {
    production: {
      plugins: ['transform-remove-console'],
    },
  },
};
```

## Memory Management

### Clear Listeners and Timers

```typescript
useEffect(() => {
  const subscription = EventEmitter.addListener('event', handler);
  const timer = setTimeout(() => {}, 1000);
  
  return () => {
    subscription.remove();
    clearTimeout(timer);
  };
}, []);
```

### Avoid Memory Leaks with Async Operations

```typescript
useEffect(() => {
  let isMounted = true;

  fetchData().then(data => {
    if (isMounted) {
      setData(data);
    }
  });

  return () => {
    isMounted = false;
  };
}, []);
```

## Text Performance

### Avoid Nested Text

```typescript
// Bad
<Text>
  <Text>Nested</Text>
  <Text>Text</Text>
</Text>

// Good
<Text>Nested Text</Text>
```

### Limit numberOfLines

```typescript
<Text numberOfLines={3} ellipsizeMode="tail">
  {longText}
</Text>
```

## Performance Monitoring

### Use Flipper

Built-in performance monitoring tool for React Native.

### Performance Monitor Overlay

```typescript
import { PerformanceMonitor } from 'react-native';

// Enable in development
if (__DEV__) {
  PerformanceMonitor.enable();
}
```

### Custom Performance Tracking

```typescript
const measurePerformance = (componentName: string) => {
  const start = performance.now();
  
  return () => {
    const duration = performance.now() - start;
    console.log(`${componentName} took ${duration}ms`);
  };
};

const MyComponent = () => {
  useEffect(() => {
    const measure = measurePerformance('MyComponent');
    return measure;
  }, []);
};
```

## Debugging Performance Issues

### Identify Slow Components

```typescript
import Profiler from 'react-native/Libraries/Utilities/Profiler';

<Profiler id="MyComponent" onRender={callback}>
  <MyComponent />
</Profiler>

function callback(
  id, // "MyComponent"
  phase, // "mount" | "update"
  actualDuration, // Time spent rendering
  baseDuration, // Estimated time without memoization
  startTime, // When rendering started
  commitTime // When committed
) {
  console.log({ id, phase, actualDuration });
}
```

## Platform-Specific Optimizations

### Android

```typescript
// Enable Hermes engine in android/app/build.gradle
project.ext.react = [
  enableHermes: true,
]

// Use ProGuard for code shrinking
android {
  buildTypes {
    release {
      minifyEnabled true
      proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
    }
  }
}
```

### iOS

```typescript
// Enable Hermes in ios/Podfile
:hermes_enabled => true

// Build optimizations
:flipper_configuration => FlipperConfiguration.disabled
```

## Best Practices Summary

1. **Use FlatList over ScrollView** for long lists
2. **Enable Hermes** JavaScript engine
3. **Memoize components** with React.memo
4. **Use useCallback** for event handlers passed to child components
5. **Use useMemo** for expensive calculations
6. **Optimize images** with proper sizing and caching
7. **Use native driver** for animations
8. **Avoid inline functions** and object literals in render
9. **Monitor performance** with profiling tools
10. **Split large components** into smaller ones
