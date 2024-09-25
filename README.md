
## Inspiration

The idea for **Signify** was sparked by the desire to create a more inclusive and accessible web experience. While traditional search engines provide options like text, voice, and image searches, there are limited solutions available for individuals who use sign language. **Signify** aims to bridge this gap by providing a search option powered by sign language recognition, allowing users to browse the web using hand gestures. Our goal is to empower the Deaf and hard-of-hearing communities with a tool that is both accessible and intuitive, while also encouraging the learning of sign language within non-deaf communities.

## What it Does

**Signify** allows users to input search queries using sign language. By leveraging hand gesture recognition technology, the platform detects the letters signed by the user and converts them into a search query. The tool then uses the **Google Custom Search API** to retrieve relevant results, providing a seamless search experience for users who rely on sign language.

## How We Built It

The project was built using:
- **React** for the front-end interface.
- **MediaPipe Hand Tracking** to detect and recognize hand gestures, translating them into letters.
- **Google Custom Search API** to handle search requests based on the signed inputs.

We started by integrating MediaPipe into the React app to capture hand movements and recognize the specific gestures for each letter in the sign language alphabet. Once recognized, the input was passed to a search bar, which then connected to the Google Custom Search API to retrieve the results based on the query.

## Challenges We Ran Into

We encountered several challenges during development:
- **Gesture Recognition Accuracy**: Ensuring that MediaPipe correctly identified hand gestures, especially for letters that are visually similar, took considerable fine-tuning. There were issues with consistency across different lighting conditions and hand positions.
- **Real-time Input**: Making sure the system could process and update search queries in real-time while maintaining performance was tricky, especially with continuous input from sign language.
- **User Experience**: Designing an intuitive interface that could handle real-time input changes without overwhelming the user required thoughtful planning and iteration.

## Accomplishments That We're Proud Of
- Successfully integrating sign language recognition with the Google Custom Search API to enable gesture-based search.
- Successfully collaborated to complete the project on time. 
- Learned more about Computer Graphics and APIs integrations into web apps. 

## What We Learned
Throughout this project, we gained a deep understanding of:
- **Gesture recognition technology** and how it can be applied to real-world problems to improve accessibility.
- The importance of designing with inclusivity in mind and creating solutions that cater to underserved communities.
- How to work with **APIs** like Google Custom Search and integrate them into an interactive platform.
- Building an accessible, real-time UI that efficiently handles user input without compromising on performance.

## What's Next for Signify
- Expand sign language support to include more gestures and sign languages.
- Improve gesture recognition accuracy by refining the model and adding more training data.
- Develop a mobile version of Signify to make the tool accessible on smartphones.
- Enhance real-time performance and optimize the search process for faster results.
- Gather user feedback from the Deaf and hard-of-hearing communities to iterate and improve the tool.
- Collaborate with accessibility advocates to broaden Signify’s impact and raise awareness.
- Integrate LLMs to personalize user experience.

