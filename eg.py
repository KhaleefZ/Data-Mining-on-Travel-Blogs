import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from wordcloud import WordCloud
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from collections import Counter
from PIL import Image, ImageTk


class TravelBlogScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Travel Blog Scraper")
        self.root.geometry("800x600")

        self.label_location = tk.Label(root, text="Enter the location you're interested in:")
        self.label_location.pack()

        self.entry_location = tk.Entry(root)
        self.entry_location.pack()

        self.button_scrape = tk.Button(root, text="Scrape Travel Blog", command=self.scrape_travel_blog)
        self.button_scrape.pack()

        self.output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=25)
        self.output_text.pack()

        self.selected_post_index = None

        # Initialize additional frames for displaying word cloud and metrics
        self.wordcloud_canvas = tk.Canvas(root, width=500, height=250)
        self.wordcloud_canvas.pack()
        self.metrics_frame = tk.Frame(root)
        self.metrics_frame.pack()

    def scrape_travel_blog(self):
        location = self.entry_location.get().strip()
        if location:
            self.output_text.delete('1.0', tk.END)  # Clear previous output
            self.output_text.insert(tk.END, f"Scraping travel blog posts related to {location}...\n\n")
            self.root.update()  # Update the GUI to show the message

            # Construct the URL based on the location
            url = f"https://www.nomadicmatt.com/travel-blog/?s={location.replace(' ', '+')}"

            # Send a GET request to the URL
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the HTML content
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find all blog post titles and links
                post_titles = soup.find_all('h2', class_='entry-title')

                # Extract titles and links
                if post_titles:
                    self.output_text.insert(tk.END, f"Travel blog posts related to {location}:\n\n")
                    self.root.update()
                    for index, title in enumerate(post_titles, 1):
                        post_title = title.text.strip()
                        post_link = title.a['href']
                        self.output_text.insert(tk.END, f"{index}. {post_title}\n")
                        self.output_text.insert(tk.END, f"Link: {post_link}\n\n")
                        self.root.update()

                    # Prompt user for the index of the selected blog post
                    self.prompt_for_post_index(post_titles)

                else:
                    self.output_text.insert(tk.END, f"No travel blog posts found for {location}.\n")
            else:
                self.output_text.insert(tk.END, "Failed to fetch the page.\n")
        else:
            messagebox.showerror("Error", "Please enter a location.")

    def prompt_for_post_index(self, post_titles):
        input_frame = tk.Frame(self.root)
        input_frame.pack()

        index_label = tk.Label(input_frame, text="Enter the index of the blog post you want to save (e.g., 1, 2, 3, ...): ")
        index_label.pack(side=tk.LEFT)

        index_entry = tk.Entry(input_frame)
        index_entry.pack(side=tk.LEFT)

        def submit_index():
            try:
                index = int(index_entry.get())
                if 1 <= index <= len(post_titles):
                    self.selected_post_index = index
                    input_frame.destroy()

                    selected_post = post_titles[self.selected_post_index - 1]
                    blog_url = selected_post.a['href']
                    self.save_blog_post(blog_url)
                else:
                    messagebox.showwarning("Warning", "Please enter a valid index.")
            except ValueError:
                messagebox.showwarning("Warning", "Please enter a valid integer.")

        submit_button = tk.Button(input_frame, text="Submit", command=submit_index)
        submit_button.pack(side=tk.LEFT)

    def save_blog_post(self, url):
        try:
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                post_title = soup.find('h1', class_='entry-title').text.strip()
                post_content = soup.find('div', class_='entry-content').text.strip()

                filename = f"{post_title}.txt"
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(f"Title: {post_title}\n\n")
                    file.write(f"URL: {url}\n\n")
                    file.write(f"Content:\n{post_content}\n")

                self.output_text.insert(tk.END, f"Blog post saved as {filename}.\n")
                # Continue with other operations (optional)
                self.calculate_metrics(post_content)
                self.generate_word_cloud(post_content)
                self.perform_content_mining(post_content)
                self.perform_keyword_search(post_content)
            else:
                self.output_text.insert(tk.END, "Failed to fetch the blog post.\n")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the blog post: {str(e)}")

    def generate_word_cloud(self, content):
        wordcloud = WordCloud(width=500, height=250, background_color='white').generate(content)
        wordcloud_image = wordcloud.to_image()
        wordcloud_photo = ImageTk.PhotoImage(wordcloud_image)
        self.wordcloud_canvas.delete("all")
        self.wordcloud_canvas.create_image(0, 0, anchor=tk.NW, image=wordcloud_photo)
        self.wordcloud_canvas.image = wordcloud_photo  # Keep a reference to prevent garbage collection

    def calculate_metrics(self, content):
        try:
            content_lower = content.lower()

            # Prepare training data
            train_texts = [" ".join(content_lower.split()[:50])] * 2  # Use first 50 words as features
            train_labels = [1, 0]  # Assuming one example is related to travel and one is not

            # Load or train the model
            try:
                classifier = joblib.load("classifier_model.joblib")
            except FileNotFoundError:
                vectorizer = TfidfVectorizer()
                clf = SVC(kernel='linear', probability=True)
                classifier = make_pipeline(vectorizer, clf)
                classifier.fit(train_texts, train_labels)
                joblib.dump(classifier, "classifier_model.joblib")

            # Simulated true label for the given content
            true_label = 1

            # Predict the label for the content
            predicted_label = classifier.predict([" ".join(content_lower.split()[:50])])[0]

            # Determine if the prediction is TP, FP, TN, or FN
            if true_label == 1 and predicted_label == 1:
                result = "True Positive (TP)"
            elif true_label == 0 and predicted_label == 1:
                result = "False Positive (FP)"
            elif true_label == 0 and predicted_label == 0:
                result = "True Negative (TN)"
            elif true_label == 1 and predicted_label == 0:
                result = "False Negative (FN)"
            else:
                result = "Unknown"

            # Display the result
            self.output_text.insert(tk.END, f"Prediction: {result}\n")
            true_labels = [true_label]
            predicted_labels = [predicted_label]

            # Calculate confusion matrix components
            TP = sum(1 for true, pred in zip(true_labels, predicted_labels) if true == 1 and pred == 1)
            FP = sum(1 for true, pred in zip(true_labels, predicted_labels) if true == 0 and pred == 1)
            TN = sum(1 for true, pred in zip(true_labels, predicted_labels) if true == 0 and pred == 0)
            FN = sum(1 for true, pred in zip(true_labels, predicted_labels) if true == 1 and pred == 0)

            # Calculate precision, recall, and F1-score
            precision = TP / (TP + FP) if (TP + FP) > 0 else 0
            recall = TP / (TP + FN) if (TP + FN) > 0 else 0
            f1 = 2 * ((precision * recall) / (precision + recall)) if (precision + recall) > 0 else 0

            # Display metrics
            self.output_text.insert(tk.END, f"True Positives (TP): {TP}\n")
            self.output_text.insert(tk.END, f"False Positives (FP): {FP}\n")
            self.output_text.insert(tk.END, f"True Negatives (TN): {TN}\n")
            self.output_text.insert(tk.END, f"False Negatives (FN): {FN}\n")
            self.output_text.insert(tk.END, f"Precision: {precision:.2f}\n")
            self.output_text.insert(tk.END, f"Recall: {recall:.2f}\n")
            self.output_text.insert(tk.END, f"F1-score: {f1:.2f}\n")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while calculating metrics: {str(e)}")

    def perform_content_mining(self, content):
        words = content.split()

        stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
                     "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
                     "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
                     "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
                     "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as",
                     "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through",
                     "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off",
                     "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how",
                     "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not",
                     "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should",
                     "now"]
        words = [word for word in words if word.lower() not in stopwords]
        word_freq = Counter(words)
        top_words = word_freq.most_common(10)

        self.output_text.insert(tk.END, "Top 10 most frequent words:\n")
        for word, freq in top_words:
            self.output_text.insert(tk.END, f"{word}: {freq}\n")

        # Perform sentiment analysis
        blob = TextBlob(content)
        sentiment = blob.sentiment
        self.output_text.insert(tk.END, f"Sentiment: Polarity={sentiment.polarity:.2f}, Subjectivity={sentiment.subjectivity:.2f}\n")

    def perform_keyword_search(self, content):
        keyword = simpledialog.askstring("Keyword Search", "Enter a keyword to search: ")
        if keyword:
            if keyword.lower() in content.lower():
                self.output_text.insert(tk.END, f"Keyword '{keyword}' found in the blog post.\n")
                sentences = content.split('.')
                relevant_sentences = [sentence.strip() for sentence in sentences if keyword.lower() in sentence.lower()]
                self.output_text.insert(tk.END, "Sentences containing the keyword:\n")
                for sentence in relevant_sentences:
                    self.output_text.insert(tk.END, f"{sentence}\n")
            else:
                self.output_text.insert(tk.END, f"Keyword '{keyword}' not found in the blog post.\n")
        else:
            self.output_text.insert(tk.END, "Invalid keyword.\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = TravelBlogScraperApp(root)
    root.mainloop()
