# Utils: graph_few_shot_examples()
# Contains the few shot example for graph retriever
def graph_few_shot_examples():
    examples = [
    {
        "question": "Find all courses offered by the degree with degreeCode 'DSAI'",
        "query": "MATCH (d:Degree {{degreeCode: 'DSAI'}})<-[:OFFERED_BY]-(c:Course) RETURN c.courseCode, c.title",
    },
    {
        "question": "List all the prerequisites for the course 'MH3701'.",
        "query": "MATCH (c:Course {{courseCode: 'MH3701'}}) OPTIONAL MATCH (preYear:yearStanding)-[:PRE_REQUISITE_FOR]->(c) WITH c, COLLECT(preYear.year) AS yearReqs OPTIONAL MATCH (g:PrerequisiteGroup)-[:PRE_REQUISITE_FOR]->(c) OPTIONAL MATCH (g)-[:REQUIRES]->(preGroupCourse:Course) WITH c, yearReqs, g, COLLECT(DISTINCT preGroupCourse.courseCode) AS groupReqs OPTIONAL MATCH (preDirect:Course)-[:PRE_REQUISITE_FOR]->(c) WITH yearReqs, groupReqs, g, COLLECT(DISTINCT preDirect.courseCode) AS directReqs RETURN yearReqs, g.logicType AS groupLogic, g.groupId AS groupId, groupReqs, directReqs",
    },
    {
        "question": "Are there any prerequisite for SC1003?",
        "query": "MATCH (c:Course {{courseCode: 'SC1003'}}) OPTIONAL MATCH (preYear:yearStanding)-[:PRE_REQUISITE_FOR]->(c) WITH c, COLLECT(preYear.year) AS yearReqs OPTIONAL MATCH (g:PrerequisiteGroup)-[:PRE_REQUISITE_FOR]->(c) OPTIONAL MATCH (g)-[:REQUIRES]->(preGroupCourse:Course) WITH c, yearReqs, g, COLLECT(DISTINCT preGroupCourse.courseCode) AS groupReqs OPTIONAL MATCH (preDirect:Course)-[:PRE_REQUISITE_FOR]->(c) WITH yearReqs, groupReqs, g, COLLECT(DISTINCT preDirect.courseCode) AS directReqs RETURN yearReqs, g.logicType AS groupLogic, g.groupId AS groupId, groupReqs, directReqs"
    },
    {
        "question": "Prerequisite of SC3000",
        "query": "MATCH (c:Course {{courseCode: 'SC3000'}}) OPTIONAL MATCH (preYear:yearStanding)-[:PRE_REQUISITE_FOR]->(c) WITH c, COLLECT(preYear.year) AS yearReqs OPTIONAL MATCH (g:PrerequisiteGroup)-[:PRE_REQUISITE_FOR]->(c) OPTIONAL MATCH (g)-[:REQUIRES]->(preGroupCourse:Course) WITH c, yearReqs, g, COLLECT(DISTINCT preGroupCourse.courseCode) AS groupReqs OPTIONAL MATCH (preDirect:Course)-[:PRE_REQUISITE_FOR]->(c) WITH yearReqs, groupReqs, g, COLLECT(DISTINCT preDirect.courseCode) AS directReqs RETURN yearReqs, g.logicType AS groupLogic, g.groupId AS groupId, groupReqs, directReqs",
    },
    {
        "question": "Find all degrees offered by the Computer Science school with schoolCode 'CCDS'",
        "query": "MATCH (s:School {{schoolCode: 'CCDS'}})-[:OFFERS_DEGREE]->(d:Degree) RETURN d.degreeCode, d.title"
    },
    {
        "question": "Find all courses that should be taken in Year 1 Semester 1 for the Computer Science (CSC) degree programme.",
        "query": "MATCH (d:Degree {{degreeCode: 'CSC'}})-[:HAS_SCHEDULED_OFFERING]->(so:ScheduledOffering {{offeringId: 'CSC_Y1S1'}})-[:INCLUDES]-(c:Course) RETURN c.courseCode, c.title"
    },
    {
        "question": "What are the specialisation track for Computer Science (CSC) degree programme.",
        "query": "MATCH (d:Degree {{degreeCode: 'CSC'}})-[:HAS_SPECIALISATION_TRACK]->(st:SpecialisationTrack) RETURN st"
    },
    {
        "question": "Find all courses in the AI Specialisation Track for Computer Science (CSC) degree programme",
        "query": "MATCH (d:Degree {{degreeCode: 'CSC'}})-[:HAS_SPECIALISATION_TRACK]->(st:SpecialisationTrack {{specialisation_id:'CSC_Artificial_Intelligence'}})-[:CONTAINS]->(c) RETURN c"
    },
    {
        "question": "Find all courses that are of type 'Core'",
        "query": "MATCH (c:Course)-[:HAS_TYPE]->(t:Type {{typeName: 'Core'}}) RETURN c.courseCode, c.title"
    },
    {
        "question": "Find all courses requiring a year Standing of 3",
        "query": "MATCH (ys:yearStanding {{year: 'Year 3'}})-[:PRE_REQUISITE_FOR]->(c:Course) RETURN c.courseCode, c.title"
    },
    {
        "question": "Find the co-requisite for a particular course.",
        "query": "MATCH (coreq:Course)-[:CO_REQUISITE_FOR]->(c:Course {{courseCode: 'SC1004'}}) RETURN coreq.courseCode, coreq.title"
    },
    {
        "question": "Find all courses offered by a certain degree programme.",
        "query": "MATCH (d:Degree {{degreeCode: 'CSC'}})<-[:OFFERED_BY]-(c:Course) RETURN c.courseCode, c.title"
    },
    {
        "question": "I want to know more about SC1007 courses offered by Computer Science Programme.",
        "query": "MATCH (d:Degree {{degreeCode:'CSC'}})<-[:OFFERED_BY]-(c:Course {{courseCode: 'SC1007'}}) RETURN c"
    },
    {
        "question": "Tell me more about SC1007",
        "query": "MATCH (c:Course {{courseCode: 'SC1007'}}) RETURN c"
    },
    {
        "question": "Can you provide details about the course SC1003, including its prerequisites and content?",
        "query": "MATCH (c:Course {{courseCode: 'SC1003'}}) RETURN c"
    },
    {
        "question": "What are the courses I am supposed to take in Year 2 as a Computer Science student?",
        "query": "MATCH (n:ScheduledOffering {{offeringId: 'CSC_Y2S1'}})-[:INCLUDES]->(c:Course) RETURN c as course UNION MATCH (n2:ScheduledOffering {{offeringId: 'CSC_Y2S2'}})-[:INCLUDES]->(c:Course)  RETURN c as course"
    },
    {
        "question": "What are the courses I am supposed to take in Year 2 as a DSAI student?",
        "query": "MATCH (n:ScheduledOffering {{offeringId: 'DSAI_Y2S1'}})-[:INCLUDES]->(c:Course) RETURN c as course UNION MATCH (n2:ScheduledOffering {{offeringId: 'DSAI_Y2S2'}})-[:INCLUDES]->(c:Course)  RETURN c as course"
    },
    {
        "question": "What are the courses I am supposed to take in Year 1 Semester 1 as a Computer Engineering (CE) student?",
        "query": "MATCH (n:ScheduledOffering {{offeringId: 'CE_Y1S1'}})-[:INCLUDES]->(c:Course) RETURN c as course"
    },
    {
        "question": "I am a Computer Science student, what are the courses I am supposed to take in Year 3 Semester 1.",
        "query": "MATCH (n:ScheduledOffering {{offeringId: 'CSC_Y3S1'}})-[:INCLUDES]->(c:Course) RETURN c as course"
    },
    {
        "question": "Can you provide a list of the Major Prescribed Elective (MPE) courses available for the Computer Science (CSC) program?",
        "query": "MATCH (d:Degree {{degreeCode: 'CSC'}})<-[:OFFERED_BY]-(c:Course)-[:HAS_TYPE]-(t:Type {{typeName: 'MPE'}}) RETURN c as course"
    },
    {
        "question": "Can you list all 3k Computer Science Courses without description?",
        "query": "MATCH(d:Degree {degreeCode:'CSC'})<-[:OFFERED_BY]-(c) WHERE c.courseCode STARTS WITH 'SC3' OR c.courseCode STARTS WITH 'MH3' OR c.courseCode STARTS WITH 'AB3' RETURN c.courseCode, c.title"
    },
    {
        "question": "What are the 4k modules available in DSAI degree?",
        "query": "MATCH(d:Degree {degreeCode:'DSAI'})<-[:OFFERED_BY]-(c) WHERE c.courseCode STARTS WITH 'SC4' OR c.courseCode STARTS WITH 'MH4' OR c.courseCode STARTS WITH 'AB4' RETURN c.courseCode, c.title"
    },
    {
        "question": "List down all the 4k modules offered by the Computer Engineering Programmer (CE)",
        "query": "MATCH(d:Degree {degreeCode:'CE'})<-[:OFFERED_BY]-(c) WHERE c.courseCode STARTS WITH 'SC4' OR c.courseCode STARTS WITH 'MH4' OR c.courseCode STARTS WITH 'AB4' RETURN c.courseCode, c.title"
    },
    {
        "question": "Can you tell me all the 4k courses offered by Business and Computer Science Double Degree (BCG) degree programme?",
        "query": "MATCH(d:Degree {degreeCode:'BCG'})<-[:OFFERED_BY]-(c) WHERE c.courseCode STARTS WITH 'SC4' OR c.courseCode STARTS WITH 'MH4' OR c.courseCode STARTS WITH 'AB4' RETURN c.courseCode, c.title"
    },
    {
        "question": "As a Computer Science student, how many academic units do I have to complete before graduation?",
        "query": "MATCH (n:Degree {degreeCode: 'CSC'})-[:HAS_AU_REQUIREMENTS]->(a:AURequirement {AUCode: 'CSC_TOTAL'}) RETURN a.Total as TotalAcademicUnits"
    },
    {
        "question": "Can you recommend me some Artificial intelligence courses offered by the Computer Science Programme?", 
        "query": "MATCH (d: Degree {{degreeCode: 'CSC'}})-[:HAS_SPECIALISATION_TRACK]->(s: SpecialisationTrack {{specialisation_id: ,'CSC_Artificial_Intelligence'}})-[:CONTAINS]->(c) RETURN c.courseCode, c.title"
    },
    {
        "question": "List down all courses in the AI Specialisation Track for Computer Science (CSC) degree programme",
        "query": "MATCH (d: Degree {{degreeCode: 'CSC'}})-[:HAS_SPECIALISATION_TRACK]->(s: SpecialisationTrack {{specialisation_id: 'CSC_Artificial_Intelligence'}})-[:CONTAINS]->(c) RETURN c.courseCode, c.title"
    },
    {
        "question": "What are the math related courses that are compulsory for a Computer Science (CSC) student?",
        "query": "MATCH (c:Course)-[:HAS_TYPE]->(t: Type {{typeName: 'Core'}}) MATCH (c)-[:OFFERED_BY]->(d: Degree {{degreeCode: 'CSC'}}) WHERE c.scope = 'MATH' OR c.courseCode STARTS WITH 'MH' RETURN c.courseCode, c.title"
    },
    {
        "question": "How many math related courses are compulsory for a Computer Science (CSC) student.",
        "query": "MATCH (c:Course)-[:HAS_TYPE]->(t: Type {{typeName: 'Core'}}) MATCH (c)-[:OFFERED_BY]->(d: Degree {{degreeCode: 'CSC'}}) WHERE c.scope = 'MATH' OR c.courseCode STARTS WITH 'MH' RETURN COUNT(c)",
    },
    {
        "question": "I am a Computer Science student, can you recommend some courses in the Artificial Intelligence Specialisation Track.",
        "query": "MATCH (d: Degree {{degreeCode: 'CSC'}})-[:HAS_SPECIALISATION_TRACK]->(s: SpecialisationTrack {{specialisation_id: 'CSC_Artificial_Intelligence'}})-[:CONTAINS]->(c) RETURN c.courseCode, c.title"
    }
    ]
    return examples