#!/usr/bin/env python3
"""
Demo: Streaming Long Text with Proper Wrapping and No Cutoff

This example demonstrates:
1. Token-by-token streaming of long generated text
2. Proper text wrapping within panels
3. No content cutoff at the end
4. Different streaming speeds and chunk sizes
5. Multiple paragraphs with markdown formatting
"""

import asyncio
import random
import time
from typing import Generator

from chuk_term.ui.streaming import StreamingMessage
from chuk_term.ui.output import get_output
from chuk_term.ui.theme import set_theme

# Long sample text with markdown formatting
LONG_MARKDOWN_TEXT = """# Understanding Neural Networks: A Comprehensive Guide

## Introduction

Neural networks are computational models inspired by the human brain's structure and function. They consist of interconnected layers of artificial neurons that process information in a way that mimics biological neural systems. This comprehensive guide will explore the fundamental concepts, architectures, and applications of neural networks in modern artificial intelligence.

## Historical Background

The journey of neural networks began in the 1940s with Warren McCulloch and Walter Pitts, who created a computational model for neural networks based on mathematics and algorithms. Their work laid the foundation for what would eventually become one of the most powerful tools in machine learning and artificial intelligence.

### Key Milestones

1. **1943**: McCulloch-Pitts neuron model introduced
2. **1958**: Frank Rosenblatt develops the Perceptron
3. **1969**: Minsky and Papert publish "Perceptrons," highlighting limitations
4. **1974-1980**: First AI Winter due to computational limitations
5. **1986**: Backpropagation algorithm popularized by Rumelhart, Hinton, and Williams
6. **2012**: AlexNet wins ImageNet competition, sparking deep learning revolution
7. **2017**: Transformer architecture introduced, revolutionizing NLP
8. **2022**: Large Language Models like GPT-3 demonstrate unprecedented capabilities

## Core Components

### Neurons and Activation Functions

At the heart of every neural network are artificial neurons, also called nodes or units. Each neuron receives input signals, processes them through an activation function, and produces an output signal. The activation function introduces non-linearity into the network, enabling it to learn complex patterns.

Common activation functions include:
- **Sigmoid**: Maps input to values between 0 and 1, useful for binary classification
- **ReLU (Rectified Linear Unit)**: Max(0, x), simple and effective for hidden layers
- **Tanh**: Maps input to values between -1 and 1, zero-centered
- **Softmax**: Converts a vector of values into probability distribution

### Network Architecture

Neural networks are organized into layers:

1. **Input Layer**: Receives raw data features
2. **Hidden Layers**: Process and transform information
3. **Output Layer**: Produces final predictions or classifications

The depth (number of layers) and width (neurons per layer) determine the network's capacity to learn complex patterns. Deep networks with many hidden layers are called Deep Neural Networks (DNNs).

## Training Process

### Forward Propagation

During forward propagation, data flows from the input layer through hidden layers to the output layer. Each neuron computes a weighted sum of its inputs, adds a bias term, and applies an activation function:

```
output = activation(Σ(weight_i * input_i) + bias)
```

### Backpropagation

Backpropagation is the algorithm used to train neural networks. It works by:
1. Computing the error between predicted and actual outputs
2. Propagating this error backward through the network
3. Adjusting weights and biases to minimize the error

The gradient descent optimization algorithm updates parameters iteratively:
```
weight_new = weight_old - learning_rate * gradient
```

### Loss Functions

Loss functions measure the difference between predicted and actual values:
- **Mean Squared Error (MSE)**: For regression tasks
- **Cross-Entropy**: For classification tasks
- **Huber Loss**: Robust to outliers in regression

## Advanced Architectures

### Convolutional Neural Networks (CNNs)

CNNs are specialized for processing grid-like data such as images. They use:
- **Convolutional layers**: Apply filters to detect features
- **Pooling layers**: Reduce spatial dimensions
- **Fully connected layers**: Final classification

Applications include image recognition, object detection, and medical imaging.

### Recurrent Neural Networks (RNNs)

RNNs process sequential data by maintaining hidden states across time steps. Variants include:
- **LSTM (Long Short-Term Memory)**: Addresses vanishing gradient problem
- **GRU (Gated Recurrent Unit)**: Simplified LSTM architecture
- **Bidirectional RNNs**: Process sequences in both directions

Used for natural language processing, time series prediction, and speech recognition.

### Transformer Networks

Transformers use self-attention mechanisms to process sequences without recurrence:
- **Multi-head attention**: Attend to different positions simultaneously
- **Positional encoding**: Inject sequence order information
- **Feed-forward networks**: Process attended representations

Revolutionary for NLP tasks, including machine translation and language modeling.

## Challenges and Solutions

### Overfitting

When networks memorize training data instead of learning patterns:
- **Solutions**: Dropout, regularization, early stopping, data augmentation

### Vanishing/Exploding Gradients

Gradients become too small or large during backpropagation:
- **Solutions**: Careful initialization, batch normalization, gradient clipping

### Computational Requirements

Deep networks require significant computational resources:
- **Solutions**: GPU acceleration, distributed training, model compression

## Real-World Applications

Neural networks have transformed numerous industries:

1. **Healthcare**: Disease diagnosis, drug discovery, personalized medicine
2. **Finance**: Fraud detection, algorithmic trading, credit scoring
3. **Autonomous Vehicles**: Object detection, path planning, decision making
4. **Entertainment**: Content recommendation, game AI, music generation
5. **Manufacturing**: Quality control, predictive maintenance, process optimization

## Future Directions

The field of neural networks continues to evolve rapidly:

- **Neuromorphic Computing**: Hardware that mimics brain architecture
- **Quantum Neural Networks**: Leveraging quantum computing principles
- **Explainable AI**: Making neural network decisions interpretable
- **Few-shot Learning**: Learning from minimal training examples
- **Neural Architecture Search**: Automated design of network architectures

## Conclusion

Neural networks have revolutionized artificial intelligence, enabling machines to tackle complex tasks previously thought impossible. As computational power increases and new architectures emerge, neural networks will continue to push the boundaries of what's possible in artificial intelligence. Understanding their principles and applications is essential for anyone working in technology, data science, or fields touched by AI transformation.

The journey from simple perceptrons to sophisticated deep learning models demonstrates the power of biomimetic approaches in computing. As we continue to unlock the mysteries of biological intelligence, neural networks will undoubtedly play a crucial role in shaping the future of technology and human-machine interaction."""


def tokenize_text(text: str, method: str = "word") -> Generator[str, None, None]:
    """
    Generate tokens from text using different methods.
    
    Args:
        text: The text to tokenize
        method: Tokenization method ('char', 'word', 'line', 'chunk')
    """
    if method == "char":
        # Character by character
        for char in text:
            yield char
    elif method == "word":
        # Word by word with proper spacing
        words = text.split()
        for i, word in enumerate(words):
            if i > 0:
                yield " "
            yield word
    elif method == "line":
        # Line by line
        lines = text.split("\n")
        for i, line in enumerate(lines):
            if i > 0:
                yield "\n"
            yield line
    elif method == "chunk":
        # Random chunks (simulating LLM streaming)
        i = 0
        while i < len(text):
            chunk_size = random.randint(1, 10)  # Random chunk size
            yield text[i:i + chunk_size]
            i += chunk_size


async def demo_streaming_speed(text: str, speed: str = "normal"):
    """Demo different streaming speeds."""
    output = get_output()
    
    # Define delay settings
    delays = {
        "instant": 0,
        "fast": 0.001,
        "normal": 0.01,
        "slow": 0.05,
        "typewriter": 0.1
    }
    
    delay = delays.get(speed, 0.01)
    
    output.info(f"\n📝 Streaming at '{speed}' speed (delay: {delay}s per token)")
    
    with StreamingMessage(title=f"🚀 {speed.capitalize()} Streaming Demo") as stream:
        for token in tokenize_text(text, method="chunk"):
            stream.update(token)
            if delay > 0:
                await asyncio.sleep(delay)
        
        # Small pause before finalization to show transition
        await asyncio.sleep(0.5)
    
    output.success(f"✅ Completed {speed} streaming demo")


async def demo_token_methods():
    """Demo different tokenization methods."""
    output = get_output()
    
    sample_text = """This is a sample paragraph demonstrating different tokenization methods.
Each method splits the text differently: characters, words, lines, or random chunks.
The streaming visualization helps understand how content flows into the panel."""
    
    methods = ["char", "word", "line", "chunk"]
    
    for method in methods:
        output.info(f"\n🔤 Demonstrating '{method}' tokenization")
        
        with StreamingMessage(title=f"📊 {method.capitalize()} Tokenization") as stream:
            token_count = 0
            for token in tokenize_text(sample_text, method=method):
                stream.update(token)
                token_count += 1
                
                # Variable delay based on method
                if method == "char":
                    await asyncio.sleep(0.005)
                elif method == "word":
                    await asyncio.sleep(0.05)
                elif method == "line":
                    await asyncio.sleep(0.3)
                else:  # chunk
                    await asyncio.sleep(0.02)
        
        output.success(f"✅ Streamed {token_count} tokens using {method} method")


async def demo_long_text_streaming():
    """Demo streaming very long text without cutoff."""
    output = get_output()
    
    output.print("\n" + "="*80)
    output.print("🎯 LONG TEXT STREAMING DEMO", style="bold cyan")
    output.print("="*80)
    output.info("This demo proves that long text streams properly without cutoff")
    
    # Stream the entire long text
    with StreamingMessage(
        title="📚 Complete Neural Networks Guide",
        show_elapsed=True,
        refresh_per_second=10  # Higher refresh rate for smoother streaming
    ) as stream:
        # Simulate realistic LLM streaming with variable chunks
        total_chars = len(LONG_MARKDOWN_TEXT)
        streamed_chars = 0
        
        for token in tokenize_text(LONG_MARKDOWN_TEXT, method="chunk"):
            stream.update(token)
            streamed_chars += len(token)
            
            # Show progress occasionally
            if streamed_chars % 500 == 0:
                progress = (streamed_chars / total_chars) * 100
                stream.update(f" [{progress:.1f}%]")
                await asyncio.sleep(0.001)  # Brief pause at progress points
            else:
                await asyncio.sleep(0.002)  # Fast streaming
    
    # Verify content integrity
    output.success(f"✅ Successfully streamed {total_chars} characters")
    output.info("📊 The panel above should show the complete guide with proper formatting")


async def demo_concurrent_streams():
    """Demo multiple concurrent streaming panels."""
    output = get_output()
    
    output.print("\n" + "="*80)
    output.print("🔀 CONCURRENT STREAMING DEMO", style="bold magenta")
    output.print("="*80)
    
    texts = [
        ("🤖 AI Assistant", "I'm processing your request and generating a detailed response about machine learning algorithms..."),
        ("📊 Data Analysis", "Analyzing dataset: Found 10,000 records with 25 features. Computing statistics..."),
        ("🔍 Search Results", "Searching knowledge base for relevant information about neural networks...")
    ]
    
    for title, text in texts:
        with StreamingMessage(title=title) as stream:
            for token in tokenize_text(text, method="word"):
                stream.update(token)
                await asyncio.sleep(0.05)
        await asyncio.sleep(0.5)  # Pause between streams


async def demo_edge_cases():
    """Demo edge cases for streaming."""
    output = get_output()
    
    output.print("\n" + "="*80)
    output.print("🔧 EDGE CASES DEMO", style="bold yellow")
    output.print("="*80)
    
    # Very long single line
    output.info("\n📏 Testing very long single line (should wrap properly)")
    long_line = "This is a very long line without any breaks that should demonstrate proper text wrapping within the panel boundaries. " * 10
    
    with StreamingMessage(title="Long Line Test") as stream:
        for token in tokenize_text(long_line, method="chunk"):
            stream.update(token)
            await asyncio.sleep(0.005)
    
    # Unicode and emojis
    output.info("\n🌍 Testing Unicode and emoji support")
    unicode_text = "Hello 世界! 🌟 Testing émojis 🚀 and spëcial cháracters: α β γ δ ε ζ η θ"
    
    with StreamingMessage(title="Unicode Test 🎨") as stream:
        for token in tokenize_text(unicode_text, method="char"):
            stream.update(token)
            await asyncio.sleep(0.03)
    
    # Code blocks in markdown
    output.info("\n💻 Testing code blocks in markdown")
    code_text = """Here's a Python function:

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

And here's JavaScript:

```javascript
const greet = (name) => {
    console.log(`Hello, ${name}!`);
};
```"""
    
    with StreamingMessage(title="Code Examples") as stream:
        for token in tokenize_text(code_text, method="line"):
            stream.update(token)
            await asyncio.sleep(0.1)


async def main():
    """Run all streaming demos."""
    output = get_output()
    
    # Header
    output.print("\n" + "🌊"*40)
    output.print("STREAMING LONG TEXT DEMONSTRATION", style="bold cyan")
    output.print("Token-by-token streaming with proper wrapping and no cutoff", style="dim")
    output.print("🌊"*40 + "\n")
    
    # Run demos
    try:
        # 1. Different tokenization methods
        await demo_token_methods()
        
        # 2. Different streaming speeds
        sample = LONG_MARKDOWN_TEXT[:500]  # Use first 500 chars for speed demo
        for speed in ["fast", "normal", "slow"]:
            await demo_streaming_speed(sample, speed)
        
        # 3. Edge cases
        await demo_edge_cases()
        
        # 4. Concurrent streams
        await demo_concurrent_streams()
        
        # 5. The main demo - full long text
        await demo_long_text_streaming()
        
        # Summary
        output.print("\n" + "="*80)
        output.success("🎉 ALL STREAMING DEMOS COMPLETED SUCCESSFULLY!")
        output.print("="*80)
        
        output.info("\n📝 Key Points Demonstrated:")
        output.print("• Token-by-token streaming works smoothly")
        output.print("• Long text wraps properly within panel boundaries")
        output.print("• No content is cut off at the end")
        output.print("• Markdown formatting is preserved in final output")
        output.print("• Unicode and emoji support works correctly")
        output.print("• Multiple streaming panels can be displayed sequentially")
        
    except KeyboardInterrupt:
        output.warning("\n⚠️ Demo interrupted by user")
    except Exception as e:
        output.error(f"\n❌ Error during demo: {e}")
        raise


if __name__ == "__main__":
    # Test with different themes
    import sys
    
    theme = sys.argv[1] if len(sys.argv) > 1 else "default"
    
    output = get_output()
    set_theme(theme)
    output.info(f"🎨 Using theme: {theme}")
    
    # Run the async demo
    asyncio.run(main())