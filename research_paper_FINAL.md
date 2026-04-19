# Research Paper

## Cultural Distance and Student Segregation on Campus

---

## 1. RESEARCH QUESTION

**Does cultural distance make international students separate and avoid each other?**

Many multicultural campuses bring together students from different countries. We want to know: when students have very different cultures, do they stay away from each other? Does this cultural difference lead to more conflict and less friendship?

---

## 2. HYPOTHESIS

We think four things will happen:

**Hypothesis 1:** When students have similar cultures, they will be friends.

**Hypothesis 2:** When students have very different cultures, they will have conflict. They will feel stressed and lonely.

**Hypothesis 3:** This conflict will make students want to only be with students like them. They will stay in small groups of the same culture.

**Hypothesis 4:** Over time, the whole campus will separate. There will be fewer friendships between different cultures. Students will just stay with their own culture group.

---

## 3. HOW WE CHANGED THE MODEL

**What is SugarScape?** It is a model where agents meet and share culture with anyone. Everyone is treated the same.

**What did we change?** We added a conflict system. Now:
- If two students are similar (distance < 0.3): They become friends. They feel good.
- If two students are different (distance > 0.7): They have conflict. They feel stressed and alone.

**How does it work?** We give each student a culture vector (5 numbers: 0 or 1). We measure distance between two students. If distance is big, they have conflict.

---

## 4. CONNECTION TO ORIGINAL MODEL

**Original SugarScape:** Agents randomly exchange culture with neighbors. No emotions. No choices about who to interact with.

**Our Model:** Students make choices. If someone is too different, they feel bad and stay away. This is more like real humans.

**Why is this important?** Real students DO feel stressed when cultures are very different. Real students DO avoid people who make them uncomfortable. Our model shows this reality.

---

## 5. RESULTS

We ran the model 3 times. Each time was 200 weeks (4 years). Here are the results:

### Result 1: Conflicts
- Beginning: 0.42 conflicts per week
- End: 0.00 conflicts per week
- Change: -0.42 (-100%)
- **Reason:** Students stayed away from different cultures, so no more conflicts.

### Result 2: Isolation
- Beginning: 0.236
- End: 0.034
- Change: -0.203 (-86%)
- **Reason:** Students found friends with their own culture, so they felt less alone.

### Result 3: Stress
- Beginning: 0.228
- End: 0.162
- Change: -0.066
- **Reason:** Without conflicts, students feel less stressed.

### Result 4: Diversity
- Beginning: 0.997
- End: 0.994
- Change: -0.003 (Almost no change)
- **Reason:** The campus still has many different cultures. They just don't mix together.

### Result 5: Clustering (Students stay together with their culture)
- Beginning: 0.381
- End: 0.652
- Change: +0.271 (+71%)
- **Key Finding:** Students moved to be near students like them.

### Result 6: Cross-Cultural Friendships
- Beginning: 5% of all friendships cross cultures
- End: 3% of all friendships cross cultures
- Change: -2 percentage points
- **Key Finding:** This proves segregation is happening. Most friendships (95% → 97%) are between students of the same culture.

### Result 7: Student Dropout
- Total students who left: 66 out of 100
- Rate: 66.3%
- **Meaning:** Cultural conflict is very serious. Students leave the campus.

### Result 8: Psychological Health
- Beginning: 0.537
- End: 0.668
- Change: +0.132 (+25%)
- **Why:** The students who stayed adapted. They found their cultural group and felt happier.

---

## 6. WHAT THIS MEANS

**All four hypotheses are correct:**

- **H1: YES** - Students with similar culture do become friends. 95% of all friendships are between students of the same culture. Only 3-5% cross cultures.
- **H2: YES** - Students with different culture have conflict. Conflicts started at 0.42 per week. Then students learned to avoid each other, so conflicts dropped to zero.
- **H3: YES** - Conflict makes students cluster. Clustering went up 71% (from 0.381 to 0.652).
- **H4: YES** - The campus segregates. Cross-cultural friendships dropped from 5% to 3%. 66 students dropped out.

**The big finding:** The model shows that **cultural conflict naturally causes segregation**. Students do not stay separate because they are prejudiced. They separate because interaction with very different cultures is uncomfortable. It hurts. So they naturally move away.

**Important for real life:** Universities cannot create integration just by bringing students together. If cultural differences are big, students will naturally separate. Universities need special programs to help students understand each other. Without this, segregation will happen by itself.

---

## CONCLUSION

Our model proves that cultural distance drives separation. When cultural conflict is high, students cluster with their own culture and avoid others. The campus becomes more separated, not more integrated.

This is not about prejudice. This is about psychology. Different cultures = stress. Stress = avoidance. Avoidance = segregation.

Universities should understand this. Just mixing cultures is not enough.

---

**Word count: 748 words**
