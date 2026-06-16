# React Native Styling Guide

## Core Styling Principles

### StyleSheet Best Practices

Always use `StyleSheet.create()` for performance optimization:

```typescript
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  // Styles are validated and optimized
});
```

### Design Tokens

Create a centralized theme system:

```typescript
// constants/theme.ts
export const colors = {
  primary: '#007AFF',
  secondary: '#5856D6',
  success: '#34C759',
  danger: '#FF3B30',
  warning: '#FF9500',
  background: '#FFFFFF',
  backgroundSecondary: '#F2F2F7',
  text: '#000000',
  textSecondary: '#8E8E93',
  border: '#C6C6C8',
};

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
};

export const typography = {
  h1: { fontSize: 32, fontWeight: 'bold' as const },
  h2: { fontSize: 24, fontWeight: 'bold' as const },
  h3: { fontSize: 20, fontWeight: '600' as const },
  body: { fontSize: 16, fontWeight: 'normal' as const },
  caption: { fontSize: 12, fontWeight: 'normal' as const },
};

export const borderRadius = {
  sm: 4,
  md: 8,
  lg: 12,
  xl: 16,
  full: 9999,
};

export const shadows = {
  sm: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.18,
    shadowRadius: 1.0,
    elevation: 1,
  },
  md: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.23,
    shadowRadius: 2.62,
    elevation: 4,
  },
  lg: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.30,
    shadowRadius: 4.65,
    elevation: 8,
  },
};
```

## Layout Patterns

### Flexbox Layouts

```typescript
// Center content
const styles = StyleSheet.create({
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

// Space between items
const styles = StyleSheet.create({
  spaceBetween: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
});

// Evenly distributed
const styles = StyleSheet.create({
  distributed: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
});

// Column with gaps
const styles = StyleSheet.create({
  column: {
    flexDirection: 'column',
    gap: 16, // Modern RN supports gap
  },
});
```

### Responsive Layouts

```typescript
import { Dimensions, PixelRatio } from 'react-native';

const { width, height } = Dimensions.get('window');

// Breakpoints
const isSmallDevice = width < 375;
const isMediumDevice = width >= 375 && width < 768;
const isLargeDevice = width >= 768;

// Responsive sizing
const responsiveSize = (size: number) => {
  const scale = width / 375; // Base on iPhone X width
  const newSize = size * scale;
  return Math.round(PixelRatio.roundToNearestPixel(newSize));
};

// Usage
const styles = StyleSheet.create({
  text: {
    fontSize: responsiveSize(16),
  },
  container: {
    padding: isLargeDevice ? 32 : 16,
  },
});
```

### Grid Layouts

```typescript
const GridView = ({ items, numColumns = 2 }) => (
  <FlatList
    data={items}
    numColumns={numColumns}
    renderItem={({ item }) => <GridItem item={item} />}
    columnWrapperStyle={styles.row}
  />
);

const styles = StyleSheet.create({
  row: {
    justifyContent: 'space-between',
    marginBottom: 16,
  },
  gridItem: {
    width: (width - 48) / 2, // Account for padding
    aspectRatio: 1,
  },
});
```

## Component Styling Patterns

### Button Variants

```typescript
type ButtonVariant = 'primary' | 'secondary' | 'outline' | 'ghost';

interface ButtonProps {
  variant?: ButtonVariant;
  size?: 'sm' | 'md' | 'lg';
}

const Button: React.FC<ButtonProps> = ({ 
  variant = 'primary', 
  size = 'md',
  children 
}) => (
  <Pressable style={[styles.button, styles[variant], styles[size]]}>
    <Text style={[styles.text, styles[`${variant}Text`]]}>{children}</Text>
  </Pressable>
);

const styles = StyleSheet.create({
  button: {
    borderRadius: borderRadius.md,
    alignItems: 'center',
    justifyContent: 'center',
  },
  // Variants
  primary: {
    backgroundColor: colors.primary,
  },
  secondary: {
    backgroundColor: colors.secondary,
  },
  outline: {
    backgroundColor: 'transparent',
    borderWidth: 1,
    borderColor: colors.primary,
  },
  ghost: {
    backgroundColor: 'transparent',
  },
  // Sizes
  sm: {
    paddingVertical: spacing.xs,
    paddingHorizontal: spacing.md,
  },
  md: {
    paddingVertical: spacing.sm,
    paddingHorizontal: spacing.lg,
  },
  lg: {
    paddingVertical: spacing.md,
    paddingHorizontal: spacing.xl,
  },
  // Text styles
  text: {
    fontWeight: '600',
  },
  primaryText: {
    color: '#fff',
  },
  secondaryText: {
    color: '#fff',
  },
  outlineText: {
    color: colors.primary,
  },
  ghostText: {
    color: colors.primary,
  },
});
```

### Card Component

```typescript
const Card = ({ elevated = false, children }) => (
  <View style={[styles.card, elevated && styles.elevated]}>
    {children}
  </View>
);

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#fff',
    borderRadius: borderRadius.lg,
    padding: spacing.md,
    marginVertical: spacing.sm,
  },
  elevated: {
    ...shadows.md,
  },
});
```

## Advanced Styling Techniques

### Dynamic Styles with Props

```typescript
interface BoxProps {
  bg?: string;
  p?: number;
  m?: number;
}

const Box: React.FC<BoxProps> = ({ bg, p, m, children }) => (
  <View 
    style={{
      backgroundColor: bg,
      padding: p ? spacing[p] : undefined,
      margin: m ? spacing[m] : undefined,
    }}
  >
    {children}
  </View>
);
```

### Style Composition

```typescript
const baseButton = {
  paddingVertical: 12,
  paddingHorizontal: 24,
  borderRadius: 8,
  alignItems: 'center' as const,
};

const styles = StyleSheet.create({
  primaryButton: {
    ...baseButton,
    backgroundColor: colors.primary,
  },
  secondaryButton: {
    ...baseButton,
    backgroundColor: colors.secondary,
  },
});
```

### Conditional Styles Array

```typescript
<View 
  style={[
    styles.base,
    isActive && styles.active,
    isDisabled && styles.disabled,
    { opacity: loading ? 0.5 : 1 },
  ]}
/>
```

## Platform-Specific Styling

```typescript
const styles = StyleSheet.create({
  container: {
    ...Platform.select({
      ios: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.25,
        shadowRadius: 3.84,
      },
      android: {
        elevation: 5,
      },
    }),
  },
  text: {
    fontSize: Platform.OS === 'ios' ? 16 : 14,
  },
});
```

## Text Styling

### Typography System

```typescript
const Text = ({ variant = 'body', children, style }) => (
  <RNText style={[typography[variant], style]}>
    {children}
  </RNText>
);

// Usage
<Text variant="h1">Heading</Text>
<Text variant="body">Body text</Text>
<Text variant="caption">Small text</Text>
```

### Text Truncation

```typescript
<Text 
  numberOfLines={2} 
  ellipsizeMode="tail"
  style={styles.text}
>
  Long text that will be truncated...
</Text>
```

## Image Styling

```typescript
const styles = StyleSheet.create({
  avatar: {
    width: 50,
    height: 50,
    borderRadius: 25,
  },
  cover: {
    width: '100%',
    aspectRatio: 16 / 9,
    resizeMode: 'cover',
  },
  contain: {
    width: 200,
    height: 200,
    resizeMode: 'contain',
  },
});
```

## Dark Mode Support

```typescript
import { useColorScheme } from 'react-native';

const ThemedComponent = () => {
  const colorScheme = useColorScheme();
  const isDark = colorScheme === 'dark';

  const styles = StyleSheet.create({
    container: {
      backgroundColor: isDark ? '#000' : '#fff',
    },
    text: {
      color: isDark ? '#fff' : '#000',
    },
  });

  return <View style={styles.container}>...</View>;
};

// Or use a theme context
const lightTheme = {
  background: '#fff',
  text: '#000',
};

const darkTheme = {
  background: '#000',
  text: '#fff',
};

const theme = isDark ? darkTheme : lightTheme;
```

## Accessibility Styling

```typescript
<TouchableOpacity
  accessible={true}
  accessibilityLabel="Submit form"
  accessibilityRole="button"
  accessibilityState={{ disabled: false }}
  style={styles.button}
>
  <Text>Submit</Text>
</TouchableOpacity>
```

## Performance Tips

1. **Avoid inline styles**: Create StyleSheet objects instead
2. **Minimize re-renders**: Use `React.memo` for styled components
3. **Use transform over layout changes**: For animations
4. **Optimize images**: Use appropriate resolutions and caching
5. **Avoid nested FlatLists**: Can cause performance issues

## Common Patterns Cheat Sheet

```typescript
// Absolute positioning
position: 'absolute',
top: 0,
left: 0,
right: 0,
bottom: 0,

// Full screen
width: '100%',
height: '100%',

// Circle
width: 100,
height: 100,
borderRadius: 50,

// Horizontal line
height: 1,
backgroundColor: colors.border,
width: '100%',

// Safe area handling
paddingTop: insets.top,
paddingBottom: insets.bottom,
```
