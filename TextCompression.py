import math
from collections import Counter
import tkinter as tk
from tkinter import ttk, scrolledtext

def calculate_probabilities(text):
    freq = Counter(text)
    total = sum(freq.values())
    chars = list(freq.keys())
    probs = [freq[c] / total for c in chars]
    return chars, probs

def build_huffman_tree(chars, probs):
    nodes = [[probs[i], [chars[i], ""]] for i in range(len(chars))]
    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda x: x[0])
        small1 = nodes.pop(0)
        small2 = nodes.pop(0)
        for pair in small1[1:]:
            pair[1] = '1' + pair[1]
        for pair in small2[1:]:
            pair[1] = '0' + pair[1]
        merged = [small1[0] + small2[0]] + small1[1:] + small2[1:]
        nodes.append(merged)
    huff_tree = nodes[0][1:]
    return dict(huff_tree)

def encode_text(text, codes):
    return ''.join(codes[c] for c in text)

def decode_text(encoded, codes):
    reverse = {v: k for k, v in codes.items()}
    current = ""
    decoded = ""
    for bit in encoded:
        current += bit
        if current in reverse:
            decoded += reverse[current]
            current = ""
    return decoded

def entropy_and_efficiency(probs, codes, chars):
    entropy = -sum([probs[i] * math.log(probs[i], 2) for i in range(len(probs))])
    avg_len = sum([probs[i] * len(codes[chars[i]]) for i in range(len(chars))])
    efficiency = entropy / avg_len
    return entropy, avg_len, efficiency

def compress_text():
    text = input_text.get("1.0", tk.END).strip()
    if not text:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "⚠️ Please enter some text.")
        return

    chars, probs = calculate_probabilities(text)
    codes = build_huffman_tree(chars, probs)
    encoded = encode_text(text, codes)
    decoded = decode_text(encoded, codes)
    entropy, avg_len, efficiency = entropy_and_efficiency(probs, codes, chars)

    original_bits = len(text) * 8
    compressed_bits = len(encoded)
    compression_ratio = round(compressed_bits / original_bits * 100, 2)

    result = []
    result.append("✅ Huffman Codes:")
    for i in range(len(chars)):
        result.append(f"{chars[i]}: {probs[i]:.4f} → {codes[chars[i]]}")
    result.append("\n🧬 Original Text: " + text)
    result.append("📦 Encoded Binary: " + encoded)
    result.append("🔓 Decoded Text: " + decoded)
    result.append(f"\n📊 Entropy (H): {round(entropy, 4)}")
    result.append(f"📏 Average Code Length (L): {round(avg_len, 4)}")
    result.append(f"⚡ Efficiency: {round(efficiency * 100, 2)}%")
    result.append("\n📉 Compression Stats:")
    result.append(f"Original Size: {original_bits} bits")
    result.append(f"Compressed Size: {compressed_bits} bits")
    result.append(f"Compression Ratio: {compression_ratio}%")

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "\n".join(result))

# GUI Setup
root = tk.Tk()
root.title("🧠 Huffman Text Compressor")
root.geometry("700x600")

ttk.Label(root, text="🔤 Enter Text to Compress:", font=("Arial", 12)).pack(pady=5)
input_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=6, font=("Courier", 10))
input_text.pack(padx=10, pady=5)

ttk.Button(root, text="🚀 Compress", command=compress_text).pack(pady=10)

ttk.Label(root, text="📋 Output:", font=("Arial", 12)).pack(pady=5)
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20, font=("Courier", 10))
output_text.pack(padx=10, pady=5)

root.mainloop()