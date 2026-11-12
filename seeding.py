import duckdb

con = duckdb.connect()  # in-memory database

con.sql("""
CREATE TABLE seeding AS SELECT * FROM (VALUES
  ('@athlete_a', 'Instagram', 52000, 'shipped', 1, 340),
  ('@athlete_b', 'TikTok', 120000, 'posted', 1, 2100),
  ('@creator_c', 'Instagram', 18000, 'posted', 1, 410),
  ('@creator_d', 'TikTok', 9000, 'shipped', 0, 0),
  ('@athlete_e', 'Instagram', 230000, 'contacted', 0, 0)
) AS t(handle, platform, followers, status, posted, engagements)
""")

# Question 1: how many people per platform?
con.sql("""
SELECT platform, COUNT(*) AS people
FROM seeding
GROUP BY platform
""").show()

# Question 2: which seeded shirts turned into posts?
con.sql("""
SELECT handle, followers, engagements
FROM seeding
WHERE posted = 1
ORDER BY engagements DESC
""").show()

# Question 3: what is the average followers per platform?
con.sql("""
SELECT platform, AVG(followers) AS avg_followers
FROM seeding
GROUP BY platform
""").show()

#Question 4: what is the percentage of shipped shirts that turn into posts?
con.sql("""
SELECT AVG(posted)*100 AS pct_posted
FROM seeding
WHERE status IN ('shipped', 'posted')
""").show()

#Question 5: what is the engagement per 1,000 followers on ppl who posted
con.sql("""
SELECT handle, ROUND(engagements * 1000 / followers, 1) AS eng_per_1k
FROM seeding
WHERE posted = 1
ORDER BY eng_per_1k DESC
""").show()