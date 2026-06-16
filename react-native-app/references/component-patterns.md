# React Native Component Patterns

## Advanced Component Patterns

### Compound Components

Pattern for components that work together:

```typescript
// Card.tsx
const CardContext = createContext<{variant: string}>(null!);

export const Card = ({ variant = 'default', children }) => (
  <CardContext.Provider value={{ variant }}>
    <View style={styles[variant]}>{children}</View>
  </CardContext.Provider>
);

Card.Header = ({ children }) => {
  const { variant } = useContext(CardContext);
  return <View style={styles[`${variant}Header`]}>{children}</View>;
};

Card.Body = ({ children }) => (
  <View style={styles.body}>{children}</View>
);

// Usage
<Card variant="elevated">
  <Card.Header><Text>Title</Text></Card.Header>
  <Card.Body><Text>Content</Text></Card.Body>
</Card>
```

### Render Props

Share logic without HOCs:

```typescript
interface DataFetcherProps<T> {
  url: string;
  children: (data: T | null, loading: boolean, error: Error | null) => React.ReactNode;
}

const DataFetcher = <T,>({ url, children }: DataFetcherProps<T>) => {
  const { data, loading, error } = useAsync(() => fetch(url).then(r => r.json()));
  return <>{children(data, loading, error)}</>;
};

// Usage
<DataFetcher<User> url="/api/user">
  {(user, loading, error) => {
    if (loading) return <ActivityIndicator />;
    if (error) return <ErrorView />;
    return <UserProfile user={user} />;
  }}
</DataFetcher>
```

### Higher-Order Components

Add functionality to existing components:

```typescript
const withLoading = <P extends object>(
  Component: React.ComponentType<P>
) => {
  return ({ loading, ...props }: P & { loading: boolean }) => {
    if (loading) return <ActivityIndicator />;
    return <Component {...(props as P)} />;
  };
};

const UserList = withLoading(({ users }) => (
  <FlatList data={users} renderItem={({ item }) => <UserCard user={item} />} />
));
```

## Form Handling Patterns

### Controlled Inputs

```typescript
const LoginForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState<{email?: string; password?: string}>({});

  const validate = () => {
    const newErrors: typeof errors = {};
    if (!email.includes('@')) newErrors.email = 'Invalid email';
    if (password.length < 6) newErrors.password = 'Too short';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = () => {
    if (validate()) {
      // Submit
    }
  };

  return (
    <View>
      <TextInput
        value={email}
        onChangeText={setEmail}
        placeholder="Email"
        keyboardType="email-address"
        autoCapitalize="none"
      />
      {errors.email && <Text style={styles.error}>{errors.email}</Text>}
      
      <TextInput
        value={password}
        onChangeText={setPassword}
        placeholder="Password"
        secureTextEntry
      />
      {errors.password && <Text style={styles.error}>{errors.password}</Text>}
      
      <Button title="Login" onPress={handleSubmit} />
    </View>
  );
};
```

### Form with React Hook Form

```typescript
import { useForm, Controller } from 'react-hook-form';

const SignupForm = () => {
  const { control, handleSubmit, formState: { errors } } = useForm();

  const onSubmit = (data) => console.log(data);

  return (
    <View>
      <Controller
        control={control}
        name="email"
        rules={{ required: 'Email is required', pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/ }}
        render={({ field: { onChange, value } }) => (
          <TextInput
            value={value}
            onChangeText={onChange}
            placeholder="Email"
          />
        )}
      />
      {errors.email && <Text>{errors.email.message}</Text>}

      <Button title="Submit" onPress={handleSubmit(onSubmit)} />
    </View>
  );
};
```

## List Patterns

### Sectioned List

```typescript
const sections = [
  { title: 'A', data: ['Alice', 'Amy'] },
  { title: 'B', data: ['Bob', 'Bill'] },
];

<SectionList
  sections={sections}
  renderItem={({ item }) => <Text>{item}</Text>}
  renderSectionHeader={({ section }) => (
    <Text style={styles.header}>{section.title}</Text>
  )}
  keyExtractor={(item, index) => item + index}
/>
```

### Infinite Scroll

```typescript
const InfiniteList = () => {
  const [data, setData] = useState([]);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);

  const loadMore = async () => {
    if (loading) return;
    setLoading(true);
    const newData = await fetchPage(page);
    setData([...data, ...newData]);
    setPage(page + 1);
    setLoading(false);
  };

  return (
    <FlatList
      data={data}
      renderItem={({ item }) => <Item data={item} />}
      onEndReached={loadMore}
      onEndReachedThreshold={0.5}
      ListFooterComponent={loading ? <ActivityIndicator /> : null}
    />
  );
};
```

## Modal Patterns

### Bottom Sheet Modal

```typescript
import { Modal, Animated, PanResponder } from 'react-native';

const BottomSheet = ({ visible, onClose, children }) => {
  const translateY = useRef(new Animated.Value(300)).current;

  useEffect(() => {
    Animated.spring(translateY, {
      toValue: visible ? 0 : 300,
      useNativeDriver: true,
    }).start();
  }, [visible]);

  return (
    <Modal transparent visible={visible} onRequestClose={onClose}>
      <TouchableWithoutFeedback onPress={onClose}>
        <View style={styles.overlay} />
      </TouchableWithoutFeedback>
      <Animated.View 
        style={[
          styles.bottomSheet, 
          { transform: [{ translateY }] }
        ]}
      >
        {children}
      </Animated.View>
    </Modal>
  );
};
```

## Error Boundary

```typescript
class ErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { hasError: boolean; error: Error | null }
> {
  state = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <View style={styles.errorContainer}>
          <Text>Something went wrong</Text>
          <Button title="Retry" onPress={() => this.setState({ hasError: false })} />
        </View>
      );
    }
    return this.props.children;
  }
}
```

## Custom Input Components

### Controlled Input with Validation

```typescript
interface InputProps {
  label: string;
  value: string;
  onChangeText: (text: string) => void;
  error?: string;
  placeholder?: string;
  secureTextEntry?: boolean;
}

const Input: React.FC<InputProps> = ({
  label,
  value,
  onChangeText,
  error,
  ...props
}) => (
  <View style={styles.inputContainer}>
    <Text style={styles.label}>{label}</Text>
    <TextInput
      style={[styles.input, error && styles.inputError]}
      value={value}
      onChangeText={onChangeText}
      {...props}
    />
    {error && <Text style={styles.errorText}>{error}</Text>}
  </View>
);
```

## Gesture Handling

### Swipeable Row

```typescript
import { PanGestureHandler } from 'react-native-gesture-handler';
import Animated, {
  useAnimatedGestureHandler,
  useAnimatedStyle,
  withSpring,
} from 'react-native-reanimated';

const SwipeableRow = ({ children, onDelete }) => {
  const translateX = useSharedValue(0);

  const gestureHandler = useAnimatedGestureHandler({
    onActive: (event) => {
      translateX.value = Math.max(event.translationX, -100);
    },
    onEnd: () => {
      if (translateX.value < -50) {
        translateX.value = withSpring(-100);
      } else {
        translateX.value = withSpring(0);
      }
    },
  });

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ translateX: translateX.value }],
  }));

  return (
    <View>
      <View style={styles.deleteButton}>
        <TouchableOpacity onPress={onDelete}>
          <Text>Delete</Text>
        </TouchableOpacity>
      </View>
      <PanGestureHandler onGestureEvent={gestureHandler}>
        <Animated.View style={animatedStyle}>
          {children}
        </Animated.View>
      </PanGestureHandler>
    </View>
  );
};
```
