import tkinter as tk
from tkinter import scrolledtext, filedialog
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urljoin

class WebCrawlerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Crawler Tool")

        # URL Entry
        self.url_label = tk.Label(root, text="Application URL:")
        self.url_label.pack(pady=5)
        self.url_entry = tk.Entry(root, width=80)
        self.url_entry.pack(pady=5)

        # Crawl Button
        self.crawl_button = tk.Button(root, text="Crawl", command=self.crawl)
        self.crawl_button.pack(pady=5)

        # Save Button
        self.save_button = tk.Button(root, text="Save to File", command=self.save_to_file)
        self.save_button.pack(pady=5)

        # Result Area
        self.result_text = scrolledtext.ScrolledText(root, width=100, height=30)
        self.result_text.pack(pady=10)

        # Store results in a variable
        self.results = ""

    def crawl(self):
        url = self.url_entry.get().strip()
        if not url:
            self.result_text.insert(tk.END, "Please enter a URL.\n")
            return

        self.result_text.delete(1.0, tk.END)  # Clear previous results
        self.result_text.insert(tk.END, f"Fetching data from: {url}\n")
        self.results = ""  # Reset results

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a', href=True)
            
            params_set = set()
            for link in links:
                href = link['href']
                full_url = urljoin(url, href)
                parsed_url = urlparse(full_url)
                params = parse_qs(parsed_url.query)
                for key in params:
                    params_set.add(key)

            if params_set:
                self.results += "Parameters found:\n"
                for param in sorted(params_set):
                    self.results += f"- {param}\n"
                    self.result_text.insert(tk.END, f"- {param}\n")
            else:
                self.results += "No parameters found.\n"
                self.result_text.insert(tk.END, "No parameters found.\n")
        except requests.RequestException as e:
            self.result_text.insert(tk.END, f"Request Error: {str(e)}\n")
        except Exception as e:
            self.result_text.insert(tk.END, f"Error: {str(e)}\n")

    def save_to_file(self):
        if not self.results:
            self.result_text.insert(tk.END, "No results to save. Please perform a crawl first.\n")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(self.results)
                self.result_text.insert(tk.END, f"Results saved to {file_path}\n")
            except IOError as e:
                self.result_text.insert(tk.END, f"Error saving file: {str(e)}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = WebCrawlerApp(root)
    root.mainloop()

