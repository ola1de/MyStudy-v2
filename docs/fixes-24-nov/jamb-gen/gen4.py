"""Batch 4: English (60) and Literature (40).
English mirrors the official JAMB Use of English structure:
comprehension 5, summary 5, cloze 10, sentence interpretation 5,
antonyms 5, synonyms 5, grammar 10, oral forms 10."""
import sys
sys.path.insert(0, "/home/hatch/workspace/mystudy/docs/fixes-24-nov/jamb-gen")
from common import Q, build, build_passage, build_poem, SRC2020

ENG_PASSAGE_COMP = ("<h3>Passage: The Cost of Honesty</h3><p>When Ada found a wallet containing a large sum of money on her way to school, she did not hesitate. She took it to the school office, where the owner, a trader who had lost it on his way to the market, was found. The trader was so grateful that he offered her a reward, but Ada refused it politely. She said that returning what does not belong to you is not a favour but a duty. Her classmates praised her, and the principal commended her before the whole school. Ada's action shows that honesty is not merely the absence of theft; it is the active choice to do what is right even when no one is watching.</p>", [
 Q("The main idea of the passage is that honesty is", ["Doing what is right even when unobserved", "Accepting rewards for good deeds", "Reporting lost property to the police", "Avoiding temptation"], 0, "Ada returned the wallet because it was her duty, not for reward.", "Comprehension/Summary", "N"),
 Q("Ada refused the trader's reward because she believed returning the wallet was", ["A duty, not a favour", "A waste of time", "The principal's order", "A way to gain fame"], 0, "She said returning what is not yours is a duty.", "Comprehension/Summary", "N"),
 Q("The word 'commended' as used in the passage is closest in meaning to", ["Praised", "Punished", "Questioned", "Ignored"], 0, "The principal commended, i.e. praised, her.", "Comprehension/Summary", "N"),
 Q("The trader lost his wallet on his way to the", ["Market", "School", "Office", "Church"], 0, "The trader lost it on his way to the market.", "Comprehension/Summary", "N"),
 Q("According to the passage, honesty is best described as", ["An active choice to do right", "The absence of theft only", "Obedience to school rules", "Fear of punishment"], 0, "Honesty is 'the active choice to do what is right'.", "Comprehension/Summary", "N"),
])

ENG_PASSAGE_SUMMARY = ("<h3>Passage: Reading for Life</h3><p>Reading is the cheapest form of travel. A single book can carry its reader across continents and centuries without the cost of a ticket. Yet many young people read only what their examinations demand. They miss the wider world that books open: the lives of others, the lessons of history, and the pleasure of language itself. A person who reads widely becomes a better thinker, because reading forces the mind to weigh ideas, compare claims and imagine alternatives. The habit is best formed early, a few pages each day, until books become companions rather than chores. A nation that reads is a nation that thinks, and a nation that thinks is a nation that grows.</p>", [
 Q("The passage suggests that young people mostly read", ["Only what examinations demand", "Books from other countries", "History books", "Poetry"], 0, "Many young people read only what examinations demand.", "Comprehension/Summary", "N"),
 Q("According to the passage, reading makes a person a better thinker because it", ["Forces the mind to weigh ideas", "Improves eyesight", "Reduces school fees", "Replaces teachers"], 0, "Reading forces the mind to weigh ideas and compare claims.", "Comprehension/Summary", "N"),
 Q("The writer compares reading to travel because books", ["Carry readers across continents and centuries", "Are sold at airports", "Require tickets", "Are written by travellers"], 0, "A book can carry its reader across continents and centuries.", "Comprehension/Summary", "N"),
 Q("The best way to form the reading habit, according to the passage, is to read", ["A few pages each day", "Only during holidays", "Whole books at once", "Only novels"], 0, "The habit is formed a few pages each day.", "Comprehension/Summary", "N"),
 Q("The passage ends with the idea that a nation that reads is a nation that", ["Grows", "Spends more", "Travels more", "Forgets its history"], 0, "A nation that reads is a nation that thinks, and grows.", "Comprehension/Summary", "N"),
])

ENG_PASSAGE_CLOZE = ("<h3>Cloze Passage: The Harmattan Morning</h3><p>The harmattan wind swept through the village, carrying dust that settled on every roof and leaf. Farmers rose early, wrapping themselves in thick cloth against the cold. In the market, traders arranged their yams and peppers, calling out to passers-by in voices made hoarse by the dry air. Children hurried to school, their lips cracked and their eyes watering. Yet the season had its gifts: the air was clear, the nights were cool, and the harvest, stored in barns, promised food for the months ahead.</p>", [
 Q("Choose the word that best completes the gap: The harmattan wind ___ through the village.", ["swept", "sleeps", "sleeping", "sweep"], 0, "Past tense 'swept' fits the narrative.", "Comprehension/Summary", "N"),
 Q("The dust settled on every roof and", ["leaf", "leaves", "leave", "leafs"], 0, "'Every roof and leaf' — singular 'leaf' matches 'every'.", "Comprehension/Summary", "N"),
 Q("Farmers rose early, wrapping themselves in thick cloth ___ the cold.", ["against", "for", "with", "to"], 0, "Cloth is worn 'against' the cold.", "Comprehension/Summary", "N"),
 Q("Traders arranged their yams and peppers, calling out to passers-by in voices made hoarse ___ the dry air.", ["by", "from", "of", "at"], 0, "Voices made hoarse 'by' the dry air.", "Comprehension/Summary", "N"),
 Q("Children hurried to school, their lips cracked and their eyes", ["watering", "watered", "waters", "water"], 0, "'Their eyes watering' is the correct participle form.", "Comprehension/Summary", "N"),
 Q("The season had its gifts: the air was clear, the nights were cool, and the harvest, stored in barns, promised food ___ the months ahead.", ["for", "to", "of", "at"], 0, "Food 'for' the months ahead.", "Comprehension/Summary", "N"),
 Q("Which word best describes the harmattan air in the passage?", ["Dry", "Humid", "Warm", "Still"], 0, "The passage stresses dry air and cracked lips.", "Comprehension/Summary", "N"),
 Q("The farmers wrapped themselves in thick cloth because the morning was", ["Cold", "Hot", "Rainy", "Dark"], 0, "They wrapped up against the cold.", "Comprehension/Summary", "N"),
 Q("The passage suggests the harmattan season is", ["Both harsh and rewarding", "Entirely harmful", "Without any effect", "The best season"], 0, "It had harsh dust and cold, but also gifts like clear air and harvest.", "Comprehension/Summary", "N"),
 Q("The main purpose of the passage is to", ["Describe a harmattan morning", "Warn against farming", "Advertise yams", "Teach children"], 0, "The passage describes a harmattan morning in a village.", "Comprehension/Summary", "N"),
])

ENGLISH_STD = [
 # Sentence interpretation (5)
 Q("Choose the interpretation: 'He is a man of his word.' This means he", ["Keeps his promises", "Talks too much", "Writes books", "Argues a lot"], 0, "A man of his word keeps his promises.", "Lexis and Structure"),
 Q("Choose the interpretation: 'The meeting was called off.' This means the meeting was", ["Cancelled", "Started", "Postponed by an hour", "Held outdoors"], 0, "Called off means cancelled.", "Lexis and Structure"),
 Q("Choose the interpretation: 'She saw through his plan.' This means she", ["Understood his true intention", "Looked at him", "Helped him", "Ignored him"], 0, "To see through a plan is to understand its real purpose.", "Lexis and Structure"),
 Q("Choose the interpretation: 'The boy is the apple of his mother's eye.' This means he is", ["Deeply loved by his mother", "A farmer", "Very tall", "Always hungry"], 0, "The apple of one's eye is someone dearly loved.", "Lexis and Structure"),
 Q("Choose the interpretation: 'We arrived in the nick of time.' This means we arrived", ["Just in time", "Very late", "Too early", "After everyone left"], 0, "In the nick of time means just in time.", "Lexis and Structure"),
 # Antonyms (5)
 Q("Choose the opposite of the underlined word: The witness gave a <u>truthful</u> account.", ["False", "Honest", "Clear", "Long"], 0, "The opposite of truthful is false.", "Lexis and Structure"),
 Q("Choose the opposite of the underlined word: The road was <u>narrow</u>.", ["Wide", "Long", "Short", "Rough"], 0, "The opposite of narrow is wide.", "Lexis and Structure"),
 Q("Choose the opposite of the underlined word: Her answer was <u>correct</u>.", ["Wrong", "Quick", "Polite", "Loud"], 0, "The opposite of correct is wrong.", "Lexis and Structure"),
 Q("Choose the opposite of the underlined word: The old man was <u>generous</u>.", ["Stingy", "Kind", "Rich", "Tall"], 0, "The opposite of generous is stingy.", "Lexis and Structure"),
 Q("Choose the opposite of the underlined word: The water is <u>clean</u>.", ["Dirty", "Cold", "Deep", "Clear"], 0, "The opposite of clean is dirty.", "Lexis and Structure"),
 # Synonyms (5)
 Q("Choose the word nearest in meaning to the underlined word: The governor's speech was <u>concise</u>.", ["Brief", "Long", "Confusing", "Angry"], 0, "Concise means brief and to the point.", "Lexis and Structure"),
 Q("Choose the word nearest in meaning to the underlined word: He is known for his <u>meticulous</u> work.", ["Careful", "Careless", "Lazy", "Hasty"], 0, "Meticulous means very careful and precise.", "Lexis and Structure"),
 Q("Choose the word nearest in meaning to the underlined word: The village was <u>deserted</u>.", ["Abandoned", "Crowded", "Beautiful", "Noisy"], 0, "Deserted means abandoned and empty.", "Lexis and Structure"),
 Q("Choose the word nearest in meaning to the underlined word: The teacher <u>praised</u> the boy.", ["Commended", "Punished", "Blamed", "Ignored"], 0, "Praised means commended.", "Lexis and Structure"),
 Q("Choose the word nearest in meaning to the underlined word: The story was <u>vivid</u>.", ["Clear and lively", "Dull", "Short", "False"], 0, "Vivid means clear and lively.", "Lexis and Structure"),
 # Basic grammar (10)
 Q("Which of the following words is correctly spelt?", ["Occurrence", "Occurence", "Ocurrence", "Occurrance"], 0, "Occurrence is the correct spelling.", "Lexis and Structure"),
 Q("Choose the correctly spelt word.", ["Separate", "Seperate", "Separete", "Separat"], 0, "Separate is the correct spelling.", "Lexis and Structure"),
 Q("Neither the teacher nor the students ___ present.", ["were", "was", "is", "has been"], 0, "With 'neither... nor', the verb agrees with the nearer subject, students, so 'were'.", "Lexis and Structure"),
 Q("Each of the boys ___ a uniform.", ["has", "have", "are having", "were"], 0, "'Each' takes a singular verb: has.", "Lexis and Structure"),
 Q("The committee ___ reached a decision.", ["has", "have", "are", "were"], 0, "Committee as one body takes 'has'.", "Lexis and Structure"),
 Q("She is the girl ___ won the prize.", ["who", "whom", "whose", "which"], 0, "'Who' is the subject pronoun for the winner.", "Lexis and Structure"),
 Q("I have lived here ___ 2015.", ["since", "for", "from", "at"], 0, "'Since' is used with a point in time, 2015.", "Lexis and Structure"),
 Q("He has been ill ___ three days.", ["for", "since", "from", "in"], 0, "'For' is used with a period of time, three days.", "Lexis and Structure"),
 Q("Choose the sentence with the correct use of the apostrophe.", ["The children's books are here.", "The childrens books are here.", "The childrens' books are here.", "The children books' are here."], 0, "Children is already plural, so the possessive is children's.", "Lexis and Structure"),
 Q("Choose the correct question tag: She can swim, ___?", ["can't she", "can she", "isn't she", "doesn't she"], 0, "The tag for 'She can swim' is 'can't she'.", "Lexis and Structure"),
 # Oral forms (10)
 Q("Choose the word with the same vowel sound as 'seat'.", ["Heat", "Hat", "Hit", "Hot"], 0, "Seat and heat share the /i:/ sound.", "Oral Forms"),
 Q("Choose the word with the same vowel sound as 'cat'.", ["Hat", "Heat", "Heart", "Hut"], 0, "Cat and hat share the /a/ sound.", "Oral Forms"),
 Q("Choose the word that rhymes with 'day'.", ["Say", "Die", "Do", "Dee"], 0, "Day and say rhyme.", "Oral Forms"),
 Q("Choose the word that rhymes with 'through'.", ["True", "Though", "Thought", "Throw"], 0, "Through and true rhyme.", "Oral Forms"),
 Q("Choose the word with a different stress pattern: 'record' as a verb is stressed on the", ["Second syllable", "First syllable", "Third syllable", "Last letter"], 0, "As a verb, record is stressed on the second syllable (re-CORD).", "Oral Forms"),
 Q("In the word 'photography', the main stress falls on the", ["Second syllable", "First syllable", "Third syllable", "Fourth syllable"], 0, "Photography is stressed on the second syllable (pho-TOG-ra-phy).", "Oral Forms"),
 Q("Choose the word in which the letter 'k' is silent.", ["Knee", "Kite", "King", "Keep"], 0, "The k in knee is silent.", "Oral Forms"),
 Q("Choose the word in which the letter 'b' is silent.", ["Comb", "Book", "Ball", "Bible"], 0, "The b in comb is silent.", "Oral Forms"),
 Q("The emphatic stress in 'I did NOT take the money' falls on", ["Not", "I", "Take", "Money"], 0, "The speaker stresses NOT to deny the act.", "Oral Forms"),
 Q("Choose the word with the consonant cluster at the beginning.", ["String", "King", "Sing", "Ring"], 0, "String begins with the cluster /str/.", "Oral Forms"),
 # Extra grammar/lexis (10) to reach 45 std
 Q("Choose the correct form: He is good ___ mathematics.", ["at", "in", "on", "for"], 0, "One is good 'at' a subject.", "Lexis and Structure"),
 Q("Choose the correct form: She congratulated him ___ his success.", ["on", "for", "at", "in"], 0, "Congratulate someone 'on' an achievement.", "Lexis and Structure"),
 Q("Which of the following sentences is correct?", ["Neither of the answers is correct.", "Neither of the answers are correct.", "Neither of the answers were correct.", "Neither of the answer is correct."], 0, "'Neither' takes a singular verb: is.", "Lexis and Structure"),
 Q("Choose the sentence that is grammatically correct.", ["The boy and his sister are here.", "The boy and his sister is here.", "The boy and his sister has come.", "The boy and his sister was here."], 0, "Two subjects joined by 'and' take a plural verb.", "Lexis and Structure"),
 Q("Choose the word that best completes the sentence: We must abide ___ the rules.", ["by", "with", "to", "in"], 0, "Abide 'by' the rules.", "Lexis and Structure"),
]

LIT_POEM = ("<b>Harmattan Morning</b><br><br>The harmattan wind sweeps the red earth,<br>and dust settles soft on roof and leaf.<br>Old women wrap their cloths close at dawn,<br>while children cough and hurry on.<br><br>The sun climbs slow, a pale gold coin,<br>through haze that hides the hills from view.<br>Yet in the barns the yams lie safe,<br>and hope, like grain, is stored there too.", [
 Q("The dominant mood of the poem is", ["Calm and hopeful", "Angry and bitter", "Joyful and loud", "Fearful and dark"], 0, "The poem is calm, ending on hope stored like grain.", "Poetry"),
 Q("The line 'the sun climbs slow, a pale gold coin' is an example of", ["Metaphor", "Simile", "Irony", "Hyperbole"], 0, "The sun is directly called a pale gold coin: metaphor.", "Poetry"),
 Q("'Dust settles soft on roof and leaf' appeals mainly to the sense of", ["Sight", "Taste", "Smell", "Hearing"], 0, "The image is visual.", "Poetry"),
 Q("The poem's setting is", ["A village in the harmattan season", "A city at night", "A riverside in the rains", "A market at noon"], 0, "Red earth, dust, barns and yams place it in a harmattan village.", "Poetry"),
 Q("The 'yams' in the barns symbolise", ["Hope and security", "Poverty", "War", "Drought"], 0, "Stored yams promise food; hope is stored with them.", "Poetry"),
])

LIT_PASSAGE = ("<b>The New Teacher</b><br><br>When Mr. Ade arrived at the village school, the pupils stared. He carried no cane, and his bag was full of books with bright covers. On his first day, he asked the class what they wanted to learn, and the room fell silent. No teacher had ever asked them that. Slowly, a small girl at the back raised her hand. 'I want to learn how to write a letter to my brother in Lagos,' she said. Mr. Ade smiled. 'Then we shall begin with letters,' he said. By the end of the term, every pupil had written a letter, and the small girl's brother had written back.", [
 Q("The pupils stared at Mr. Ade because he", ["Carried no cane and asked what they wanted to learn", "Was very tall", "Spoke a foreign language", "Arrived late"], 0, "He carried no cane and asked the class what they wanted to learn.", "Prose"),
 Q("The small girl wanted to learn how to", ["Write a letter to her brother", "Draw pictures", "Sing songs", "Count money"], 0, "She wanted to write a letter to her brother in Lagos.", "Prose"),
 Q("The passage suggests Mr. Ade was different from other teachers because he", ["Listened to his pupils", "Punished pupils", "Ignored the class", "Taught only reading"], 0, "He asked what they wanted to learn and built lessons on it.", "Prose"),
 Q("By the end of the term, every pupil had", ["Written a letter", "Left the school", "Failed the examination", "Bought a book"], 0, "By the end of the term, every pupil had written a letter.", "Prose"),
 Q("The tone of the passage can best be described as", ["Warm and hopeful", "Angry", "Suspicious", "Boring"], 0, "The story is warm: the girl's brother wrote back.", "Prose"),
])

LITERATURE_STD = [
 Q("A speech delivered by a character alone on stage is called a", ["Soliloquy", "Dialogue", "Monologue", "Aside"], 0, "A soliloquy is spoken alone on stage, revealing inner thoughts.", "Drama"),
 Q("The struggle between the protagonist and an opposing force is called", ["Conflict", "Climax", "Resolution", "Denouement"], 0, "Conflict is the struggle driving a play.", "Drama"),
 Q("The turning point of a play, where tension is highest, is the", ["Climax", "Exposition", "Resolution", "Prologue"], 0, "The climax is the peak of tension.", "Drama"),
 Q("A play that ends sadly, often with the death of the hero, is a", ["Tragedy", "Comedy", "Farce", "Melodrama"], 0, "Tragedy ends in sorrow, often death.", "Drama"),
 Q("A humorous play with a happy ending is a", ["Comedy", "Tragedy", "Elegy", "Epic"], 0, "Comedy ends happily.", "Drama"),
 Q("The main character of a play or novel is the", ["Protagonist", "Antagonist", "Foil", "Narrator"], 0, "The protagonist is the central character.", "Drama"),
 Q("The character who opposes the protagonist is the", ["Antagonist", "Hero", "Chorus", "Fool"], 0, "The antagonist works against the hero.", "Drama"),
 Q("A short remark spoken by a character to the audience, unheard by others on stage, is an", ["Aside", "Soliloquy", "Dialogue", "Epilogue"], 0, "An aside is addressed to the audience alone.", "Drama"),
 Q("The repetition of the same consonant sound at the start of words is", ["Alliteration", "Assonance", "Onomatopoeia", "Rhyme"], 0, "Alliteration repeats initial consonant sounds.", "Poetry"),
 Q("The repetition of vowel sounds within words is", ["Assonance", "Alliteration", "Consonance", "Irony"], 0, "Assonance repeats vowel sounds.", "Poetry"),
 Q("'The sun smiled down on the valley' is an example of", ["Personification", "Metaphor", "Simile", "Irony"], 0, "The sun is given human action: personification.", "Poetry"),
 Q("'He is as brave as a lion' is an example of", ["Simile", "Metaphor", "Hyperbole", "Irony"], 0, "Comparison with 'as' is a simile.", "Poetry"),
 Q("'The classroom was a zoo' is an example of", ["Metaphor", "Simile", "Personification", "Euphemism"], 0, "Direct comparison without 'like' or 'as' is a metaphor.", "Poetry"),
 Q("A word that imitates a sound, like 'buzz', is an example of", ["Onomatopoeia", "Alliteration", "Assonance", "Oxymoron"], 0, "Onomatopoeia imitates sounds.", "Poetry"),
 Q("A poem of fourteen lines with a set rhyme scheme is a", ["Sonnet", "Ballad", "Elegy", "Ode"], 0, "A sonnet has fourteen lines.", "Poetry"),
 Q("A mournful poem for the dead is an", ["Elegy", "Ode", "Ballad", "Epic"], 0, "An elegy mourns the dead.", "Poetry"),
 Q("A long narrative poem about heroic deeds is an", ["Epic", "Sonnet", "Lyric", "Haiku"], 0, "An epic tells heroic deeds at length.", "Poetry"),
 Q("The narrator's viewpoint in a novel told with 'I' is", ["First person", "Third person", "Second person", "Omniscient"], 0, "'I' narration is first person.", "Prose"),
 Q("The sequence of events in a novel is its", ["Plot", "Theme", "Setting", "Style"], 0, "Plot is the arrangement of events.", "Prose"),
 Q("The central idea of a literary work is its", ["Theme", "Plot", "Character", "Setting"], 0, "Theme is the main idea.", "General Literary Terms and Principles"),
 Q("The time and place of a story is its", ["Setting", "Plot", "Theme", "Mood"], 0, "Setting is time and place.", "General Literary Terms and Principles"),
 Q("A statement that means the opposite of what it says is", ["Irony", "Sarcasm only", "Metaphor", "Simile"], 0, "Irony says one thing and means another.", "General Literary Terms and Principles"),
 Q("Exaggeration for effect, as in 'I have told you a million times', is", ["Hyperbole", "Irony", "Litotes", "Euphemism"], 0, "Hyperbole is deliberate exaggeration.", "General Literary Terms and Principles"),
 Q("A mild expression used in place of a harsh one is a", ["Euphemism", "Hyperbole", "Irony", "Oxymoron"], 0, "Euphemism softens harsh truth.", "General Literary Terms and Principles"),
 Q("Two opposite words placed together, like 'deafening silence', form an", ["Oxymoron", "Simile", "Metaphor", "Pun"], 0, "Oxymoron joins contradictory terms.", "General Literary Terms and Principles"),
 Q("The use of symbols to represent ideas is called", ["Symbolism", "Imagery", "Allegory only", "Satire"], 0, "Symbolism uses objects to stand for ideas.", "Literary Appreciation"),
 Q("A story in which characters and events stand for deeper meanings is an", ["Allegory", "Fable", "Myth", "Legend"], 0, "Allegory carries a second, symbolic meaning.", "Literary Appreciation"),
 Q("Writing that mocks human folly to correct it is", ["Satire", "Elegy", "Ode", "Epic"], 0, "Satire uses humour and ridicule to correct.", "Literary Appreciation"),
 Q("The atmosphere or feeling created by a literary work is its", ["Mood", "Tone", "Style", "Rhythm"], 0, "Mood is the feeling a work creates in the reader.", "Literary Appreciation"),
 Q("The author's attitude towards the subject is the work's", ["Tone", "Mood", "Plot", "Setting"], 0, "Tone is the writer's attitude.", "Literary Appreciation"),
]
