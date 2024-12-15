import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "put this into a proper format for meeting minutes: Saint Andrews to donate computers to the schools\nVirtual tools and VR headphones\n\nPricing of the project: Four VR headsets\nWill be kept at Science Com\nBy Januray everything will be set\nEverything else follows after everything is done\n\n\nChristmas cards: next week\n        by monday\n        have to be signed by Koja\n        head of the departments and the rest of the team\n\n\nQuotations for the lab equipments are in\nProcurement is yet to gie the approved stuff from the vendors list\none point six M for two schools\ntryng to use a supplier not on the vendors list\n\nCareer guidance day.\n        The money is not in for the event\n        The event is still there\n        Venue issues\n        Venue options: MUBAS and MLW Nyika Rooms\n        MUBAS or KUHes for the event\n        Kuhes for the event confirmed now\n\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Okay, here's a formatted version of your notes, structured as meeting minutes:\n\n**Meeting Minutes**\n\n**Date:** [Insert Date Here]\n**Attendees:** [List Attendees Here, if known]\n**Subject:** Project Updates and Action Items\n\n**1. Computer Donation & Virtual Reality Project (Saint Andrews)**\n\n*   **Action:** Saint Andrews will be donating computers to local schools.\n*   **Action:** The project will also include virtual tools and VR headphones.\n*   **Pricing:** Four VR headsets have been acquired.\n*   **Location:** The VR headsets will be kept at the Science Communication department (Science Com).\n*   **Timeline:** Project completion (setup) is targeted for January.\n*   **Action:** Remaining project tasks will be addressed after initial setup is complete.\n\n**2. Christmas Cards**\n\n*   **Timeline:** Christmas card distribution is planned for next week.\n*   **Deadline:** Cards must be ready by Monday.\n*   **Action:** Koja is responsible for signing the cards, along with the department heads and the rest of the team.\n\n**3. Lab Equipment Procurement**\n\n*   **Status:** Quotations for lab equipment have been received.\n*   **Action:** Procurement is awaiting approval of vendor list items.\n*   **Budget:** The current budget is 1.6 million for two schools.\n*   **Issue:** There is a desire to use a supplier not currently on the approved vendors list.\n\n**4. Career Guidance Day**\n\n*   **Funding:** The funding for the Career Guidance Day event has not yet been received.\n*   **Status:** The event is still scheduled to proceed.\n*   **Issue:** Venue selection is still outstanding.\n*   **Venue Options:**\n    *   MUBAS (Malawi University of Business and Applied Sciences)\n    *   MLW Nyika Rooms (Malawi Liverpool Wellcome Trust)\n*   **Decision:** KUHes (Kamuzu University of Health Sciences) has been confirmed as the venue.\n\n**Action Items Summary:**\n\n*   **Saint Andrews Project:** Complete setup of computers and VR equipment by January.\n*   **Christmas Cards:** Prepare, sign, and distribute cards by next Monday, with Koja, Department Heads, and the team signing.\n*   **Lab Equipment:** Procurement to secure vendor approvals and resolve supplier issue.\n*   **Career Guidance Day:** Continue planning event with KUHes as confirmed venue despite funding delays.\n\n**Next Steps:**\n\n*  [Optional - Add a note on when the next meeting is]\n\n**Notes:**\n\n*   **[Insert Date Here]:** Make sure to replace this with the actual date of the meeting.\n*   **[List Attendees Here, if known]:** If you know who attended the meeting, include their names.\n*   **Action Items:** I've tried to clearly define specific action items from the points listed.\n*   **Formatting:** I've used bullet points for clarity and sub-headings to organize the information.\n*   **Clarity:** If you have more information or specifics on any of these areas, you can add them into the respective sections.\n",
      ],
    },
  ]
)

response = chat_session.send_message("INSERT_INPUT_HERE")

print(response.text)