"""
SCOUTRPG
This is a new game I've developed that simulates the life of a Boy Scout and their journey towards Eagle.
"""
import math
import time

import os
from Applications import bagels
from System import Loading
from datetime import datetime as dt, timedelta as td
import calendar
import random

# TODO
# Add attributes for all possessions (if applicable).
# Add Rank.
# Add more events to the troop meeting and increase number shown to 4.
# Ask Appa and Amma for feedback!

stats_list = ("Health", "Hunger", "Thirst", "Money")
food_list = ("peanuts", "breakfast burrito", "pancake", "mac and cheese", "tofu teriyaki")
food_costs = (0.49, 3.49, 2.49, 9.49, 14.99)
drinks_list = ("water", "soda", "tea")
drinks_cost = (0.25, 1.49, 1.99)
locations_list = ("grocery store", "department store", "scout store")
chore_list = ("unload dishwasher", "load dishwasher", "clean up bedroom", "clean up kitchen", "clean up dining room",
              "clean up living room", "collect the trash")
department_list = ("rugged pants", "rugged jacket", "full body thermals", "hiking socks", "hiking shoes", "tent", "desk",
                   "computer", "cell phone", "digital watch", "game console", "camera")
department_costs = (24.99, 19.99, 14.99, 7.49, 62.49, 49.99, 99.99,
                    499.99, 449.99, 14.99, 549.99, 199.99)
scout_store_list = ("pants", "short pants", "long-sleeve shirt", "short-sleeve shirt", "socks", "belt", "cap", "accessories",
                    "neckerchief", "slide", "shoes", "handbook", "large tent", "sleeping bag", "sleeping pad", "camping pack",
                    "hiking sticks", "day pack", "scout water bottle", "insect repellent", "sunscreen", "compass",
                    "first aid kit", "pillow", "mess kit", "drinking cup")
scout_store_costs = (59.99, 23.99, 37.99, 26.99, 14.99, 19.99, 24.99, 19.99,
                     23.99, 14.99, 29.99, 27.49, 149.99, 49.99, 42.49, 34.99,
                     19.99, 34.99, 14.99, 9.99, 9.99, 14.99,
                     19.99, 24.99, 14.99, 7.49)
possession_attributes = {"computer": "ScoutRPG.online_shopping = True",
                         "cell phone": "ScoutRPG.sleep_weight.extend([0] * 2 + [1] * 2) ; ScoutRPG.choices['self.phone()'] = 'phone'",
                         "digital watch": "ScoutRPG.sleep_weight.extend([0] * 6 + [1] * 7)",
                         "game console": "ScoutRPG.sleep_weight.extend([3] * 3 + [4] * 2) ; ScoutRPG.choices['self.console()'] = 'console'",
                         "camera": "ScoutRPG.sleep_weight.extend([4]) ; ScoutRPG.memories = True"}
event_list = { "small hike": "self.hike('small')", "first aid": "self.first_aid()", "orienteering": "self.orienteering()", "knot training": "self.knot_training()",
              "hike": "self.hike('big')", "rock climbing": "self.rock_climbing()", "coastal cleanup": "self.coastal_cleanup()", "bowling": "self.bowling()", "escape room": "self.escape_room()",
              "cert outing": "self.cert_outing()", "kids against hunger": "self.kids_against_hunger()", "conservation outing": "self.conservation_outing()"}
# "troop meeting": "self.troop_meeting()",

# noinspection LongLine
ranks = {
    "scout": (
        "1a. Repeat from memory the Scout Oath, Scout Law, Scout motto, and Scout slogan. In your own words, explain their meaning. ",
        "1b. Explain what Scout spirit is. Describe some ways you have shown Scout spirit by practicing the Scout Oath, Scout Law, Scout motto, and Scout slogan.",
        "1c. Demonstrate the Scout sign, salute, and handshake. Explain when they should be used.",
        "1d. Describe the First Class Scout badge and tell what each part stands for. Explain the significance of the First Class Scout badge.",
        "1e. Repeat from memory the Outdoor Code. In your own words, explain what the Outdoor Code means to you.",
        "1f. Repeat from memory the Pledge of Allegiance. In your own words, explain its meaning.",
        "2. After attending at least one Scout troop meeting, do the following:",
        "2a. Describe how the Scouts in the troop provide its leadership.",
        "2b. Describe the four steps of Scout advancement.",
        "2c. Describe what the Scouts BSA ranks are and how they are earned.",
        "2d. Describe what merit badges are and how they are earned.",
        "3a. Explain the patrol method. Describe the types of patrols that are used in your troop.",
        "3b. Become familiar with your patrol name, emblem, flag, and yell. Explain how these items create patrol spirit.",
        "4a. Show how to tie a square knot, two half-hitches, and a taut-line hitch. Explain how each knot is used.",
        "4b. Show the proper care of a rope by learning how to whip and fuse the ends of different kinds of rope. ",
        "5. Tell what you need to know about pocketknife safety. ",
        "6. With your parent or guardian, complete the exercises in the pamphlet How to Protect Your Children From Child Abuse: A Parent’s Guide and earn the Cyber Chip Award for your grade.",
        "7. Since joining the troop and while working on the Scout rank, participate in a Scoutmaster conference."),
    "tenderfoot": (
        "1a. Present yourself to your leader, prepared for an overnight camping trip. Show the personal and camping gear you will use. Show the right way to pack and carry it.",
        "1b. Spend at least one night on a patrol or troop campout. Sleep in a tent you have helped pitch.",
        "1c. Tell how you practiced the Outdoor Code on a campout or outing.",
        "2a. On the campout, assist in preparing one of the meals. Tell why it is important for each patrol member to share in meal preparation and cleanup.",
        "2b. While on a campout, demonstrate the appropriate method of safely cleaning items used to prepare, serve, and eat a meal.",
        "2c. Explain the importance of eating together as a patrol.",
        "3a. Demonstrate a practical use of the square knot.",
        "3b. Demonstrate a practical use of two half-hitches.",
        "3c. Demonstrate a practical use of the taut-line hitch.",
        "3d. Demonstrate proper care, sharpening, and use of the knife, saw, and ax. Describe when each should be used.",
        "4a. Show first aid for the following: \n• Simple cuts and scrapes\n• Blisters on the hand and foot\n• Minor (thermal/heat) burns or scalds (superficial, or first-degree)\n• Bites or stings of insects and ticks\n• Venomous snakebite\n• Nosebleed\n• Frostbite and sunburn\n• Choking",
        "4b. Describe common poisonous or hazardous plants; identify any that grow in your local area or campsite location. Tell how to treat for exposure to them.",
        "4c. Tell what you can do while on a campout or other outdoor activity to prevent or reduce the occurrence of injuries or exposure listed in Tenderfoot requirements 4a and 4b.",
        "4d. Assemble a personal first-aid kit to carry with you on future campouts and hikes. Tell how each item in the kit would be used.",
        "5a. Explain the importance of the buddy system as it relates to your personal safety on outings and in your neighborhood. Use the buddy system while on a troop or patrol outing.",
        "5b. Describe what to do if you become lost on a hike or campout.",
        "5c. Explain the rules of safe hiking, both on the highway and cross-country, during the day and at night.",
        "6a. Record your best in the following tests:\n• Pushups (Record the number done correctly in 60 seconds.)\n• Situps or curl-ups (Record the number done correctly in 60 seconds.)\n• Back-saver sit-and-reach (Record the distance stretched.)\n• 1-mile walk/run (Record the time.)",
        "6b. Develop and describe a plan for improvement in each of the activities listed in Tenderfoot requirement 6a. Keep track of your activity for at least 30 days.",
        "6c. Show improvement (of any degree) in each activity listed in Tenderfoot requirement 6a after practicing for 30 days.\n• Pushups (Record the number done correctly in 60 seconds.)\n• Situps or curl-ups (Record the number done correctly in 60 seconds.)\n• Back-saver sit-and-reach (Record the distance stretched.)\n• 1-mile walk/run (Record the time.)",
        "7a. Demonstrate how to display, raise, lower, and fold the U.S. flag.",
        "7b. Participate in a total of one hour of service in one or more service projects approved by your Scoutmaster. Explain how your service to others relates to the Scout slogan and Scout motto.",
        "8. Describe the steps in Scouting’s Teaching EDGE method. Use the Teaching EDGE method to teach another person how to tie the square knot.",
        "9. Demonstrate Scout spirit by living the Scout Oath and Scout Law. Tell how you have done your duty to God and how you have lived four different points of the Scout Law in your everyday life.",
        "10. While working toward the Tenderfoot rank, and after completing Scout rank requirement 7, participate in a Scoutmaster conference.",
        "11. Successfully complete your board of review for the Tenderfoot rank."),
    "second class": (
        "1a. Since joining Scouts BSA, participate in five separate troop/patrol activities, at least three of which must be held outdoors. Of the outdoor activities, at least two must include overnight camping. These activities do not include troop or patrol meetings. On campouts, spend the night in a tent that you pitch or other structure that you help erect, such as a lean-to, snow cave, or tepee.",
        "1b. Explain the principles of Leave No Trace and tell how you practiced them on a campout or outing. This outing must be different from the one used for Tenderfoot requirement 1c.",
        "1c. On one of these campouts, select a location for your patrol site and recommend it to your patrol leader, senior patrol leader, or troop guide. Explain what factors you should consider when choosing a patrol site and where to pitch a tent.",
        "2a. Explain when it is appropriate to use a fire for cooking or other purposes and when it would not be appropriate to do so.",
        "2b. Use the tools listed in Tenderfoot requirement 3d to prepare tinder, kindling, and fuel wood for a cooking fire.",
        "2c. At an approved outdoor location and time, use the tinder, kindling, and fuel wood from Second Class requirement 2b to demonstrate how to build a fire. Unless prohibited by local fire restrictions, light the fire. After allowing the flames to burn safely for at least two minutes, safely extinguish the flames with minimal impact to the fire site.",
        "2d. Explain when it is appropriate to use a lightweight stove and when it is appropriate to use a propane stove. Set up a lightweight stove or propane stove. Light the stove, unless prohibited by local fire restrictions. Describe the safety procedures for using these types of stoves.",
        "2e. On one campout, plan and cook one hot breakfast or lunch, selecting foods from MyPlate or the current USDA nutritional model. Explain the importance of good nutrition. Demonstrate how to transport, store, and prepare the foods you selected.",
        "2f. Demonstrate tying the sheet bend knot. Describe a situation in which you would use this knot.",
        "2g. Demonstrate tying the bowline knot. Describe a situation in which you would use this knot.",
        "3a. Demonstrate how a compass works and how to orient a map. Use a map to point out and tell the meaning of five map symbols.",
        "3b. Using a compass and map together, take a 5-mile hike (or 10 miles by bike) approved by your adult leader and your parent or guardian.",
        "3c. Describe some hazards or injuries that you might encounter on your hike and what you can do to help prevent them.",
        "3d. Demonstrate how to find directions during the day and at night without using a compass or an electronic device.",
        "4. Identify or show evidence of at least 10 kinds of wild animals (such as birds, mammals, reptiles, fish, or mollusks) found in your local area or camping location. You may show evidence by tracks, signs, or photographs you have taken.",
        "5a. Tell what precautions must be taken for a safe swim.",
        "5b. Demonstrate your ability to pass the BSA beginner test: Jump feet first into water over your head in depth, level off and swim 25 feet on the surface, stop, turn sharply, resume swimming, then return to your starting place.",
        "5c. Demonstrate water rescue methods by reaching with your arm or leg, by reaching with a suitable object, and by throwing lines and objects.",
        "5d. Explain why swimming rescues should not be attempted when a reaching or throwing rescue is possible. Explain why and how a rescue swimmer should avoid contact with the victim.",
        "6a. Demonstrate first aid for the following:\n• Object in the eye\n• Bite of a warm-blooded animal\n• Puncture wounds from a splinter, nail, and fishhook\n• Serious burns (partial thickness, or second-degree)\n• Heat exhaustion\n• Shock\n• Heatstroke, dehydration, hypothermia, and hyperventilation",
        "6b. Show what to do for “hurry” cases of stopped breathing, stroke, severe bleeding, and ingested poisoning.",
        "6c. Tell what you can do while on a campout or hike to prevent or reduce the occurrence of the injuries listed in Second Class requirements 6a and 6b.",
        "6d. Explain what to do in case of accidents that require emergency response in the home and backcountry. Explain what constitutes an emergency and what information you will need to provide to a responder.",
        "6e. Tell how you should respond if you come upon the scene of a vehicular accident.",
        "7a. After completing Tenderfoot requirement 6c, be physically active at least 30 minutes each day for five days a week for four weeks. Keep track of your activities.",
        "7b. Share your challenges and successes in completing Second Class requirement 7a. Set a goal for continuing to include physical activity as part of your daily life and develop a plan for doing so.",
        "7c. Participate in a school, community, or troop program on the dangers of using drugs, alcohol, and tobacco and other practices that could be harmful to your health. Discuss your participation in the program with your family, and explain the dangers of substance addictions. Report to your Scoutmaster or other adult leader in your troop about which parts of the Scout Oath and Scout Law relate to what you learned. ",
        "8a. Participate in a flag ceremony for your school, religious institution,chartered organization, community, or Scouting activity.",
        "8b. Explain what respect is due the flag of the United States.",
        "8c. With your parents or guardian, decide on an amount of money that you would like to earn, based on the cost of a specific item you would like to purchase. Develop a written plan to earn the amount agreed upon and follow that plan; it is acceptable to make changes to your plan along the way. Discuss any changes made to your original plan and whether you met your goal.",
        "8d. At a minimum of three locations, compare the cost of the item for which you are saving to determine the best place to purchase it. After completing Second Class requirement 8c, decide if you will use the amount that you earned as originally intended, save all or part of it, or use it for another purpose.",
        "8e. Participate in two hours of service through one or more service projects approved by your Scoutmaster. Tell how your service to others relates to the Scout Oath.",
        "9a. Explain the three R’s of personal safety and protection.",
        "9b. Describe bullying; tell what the appropriate response is to someone who is bullying you or another person.",
        "10. Demonstrate Scout spirit by living the Scout Oath and Scout Law. Tell how you have done your duty to God and how you have lived four different points of the Scout Law (not to include those used for Tenderfoot requirement 9) in your everyday life.",
        "11. While working toward the Second Class rank, and after completing Tenderfoot requirement 10, participate in a Scoutmaster conference.",
        "12. Successfully complete your board of review for the Second Class rank."),
    "first class": (
        "1a. Since joining Scouts BSA, participate in 10 separate troop/patrol activities, at least six of which must be held outdoors. Of the outdoor activities, at least three must include overnight camping. These activities do not include troop or patrol meetings. On campouts, spend the night in a tent that you pitch or other structure that you help erect, such as a lean-to, snow cave, or tepee.",
        "1b. Explain each of the principles of Tread Lightly! and tell how you practiced them on a campout or outing. This outing must be different from the ones used for Tenderfoot requirement 1c and Second Class requirement 1b. 2a. Help plan a menu for one of the above campouts that includes at least one breakfast, one lunch, and one dinner, and that requires cooking at least two of the meals. Tell how the menu includes the foods from MyPlate or the current USDA nutritional model and how it meets nutritional needs for the planned activity or campout.",
        "2b. Using the menu planned in First Class requirement 2a, make a list showing a budget and the food amounts needed to feed three or more youth. Secure the ingredients.",
        "2c. Show which pans, utensils, and other gear will be needed to cook and serve these meals.",
        "2d. Demonstrate the procedures to follow in the safe handling and storage of fresh meats, dairy products, eggs, vegetables, and other perishable food products. Show how to properly dispose of camp garbage, cans, plastic containers, and other rubbish.",
        "2e. On one campout, serve as cook. Supervise your assistant(s) in using a stove or building a cooking fire. Prepare the breakfast, lunch, and dinner planned in First Class requirement 2a. Supervise the cleanup.",
        "3a. Discuss when you should and should not use lashings.",
        "3b. Demonstrate tying the timber hitch and clove hitch.",
        "3c. Demonstrate tying the square, shear, and diagonal lashings by joining two or more poles or staves together.",
        "3d. Use lashings to make a useful camp gadget or structure.",
        "4a. Using a map and compass, complete an orienteering course that covers at least one mile and requires measuring the height and/or width of designated items (tree, tower, canyon, ditch, etc.).",
        "4b. Demonstrate how to use a handheld GPS unit, GPS app on a smartphone, or other electronic navigation system while on a campout or hike. Use GPS to find your current location, a destination of your choice, and the route you will take to get there. Follow that route to arrive at your destination.",
        "5a. Identify or show evidence of at least 10 kinds of native plants found in your local area or campsite location. You may show evidence by identifying fallen leaves or fallen fruit that you find in the field, or as part of a collection you have made, or by photographs you have taken.",
        "5b. Identify two ways to obtain a weather forecast for an upcoming activity. Explain why weather forecasts are important when planning for an event.",
        "5c. Describe at least three natural indicators of impending hazardous weather, the potential dangerous events that might result from such weather conditions, and the appropriate actions to take.",
        "5d. Describe extreme weather conditions you might encounter in the outdoors in your local geographic area. Discuss how you would determine ahead of time the potential risk of these types of weather dangers, alternative planning considerations to avoid such risks, and how you would prepare for and respond to those weather conditions.",
        "6a. Successfully complete the BSA swimmer test.",
        "6b. Tell what precautions must be taken for a safe trip afloat.",
        "6c. Identify the basic parts of a canoe, kayak, or other boat. Identify the parts of a paddle or an oar.",
        "6d. Describe proper body positioning in a watercraft, depending on the type and size of the vessel. Explain the importance of proper body position in the boat.",
        "6e. With a helper and a practice victim, show a line rescue both as tender and as rescuer. (The practice victim should be approximately 30 feet from shore in deep water.)",
        "7a. Demonstrate bandages for a sprained ankle and for injuries on the head, the upper arm, and the collarbone.",
        "7b. By yourself and with a partner, show how to:",
        "• Transport a person from a smoke-filled room.",
        "• Transport for at least 25 yards a person with a sprained ankle.",
        "7c. Tell the five most common signals of a heart attack. Explain the steps (procedures) in cardiopulmonary resuscitation (CPR)."
        "7d. Tell what utility services exist in your home or meeting place. Describe potential hazards associated with these utilities and tell how to respond in emergency situations.",
        "7e. Develop an emergency action plan for your home that includes what to do in case of fire, storm, power outage, and water outage."
        "7f. Explain how to obtain potable water in an emergency.",
        "8a. After completing Second Class requirement 7a, be physically active at least 30 minutes each day for five days a week for four weeks. Keep track of your activities.",
        "8b. Share your challenges and successes in completing First Class requirement 8a. Set a goal for continuing to include physical activity as part of your daily life.",
        "9a. Visit and discuss with a selected individual approved by your leader (for example, an elected official, judge, attorney, civil servant, principal, or teacher) the constitutional rights and obligations of a U.S. citizen.",
        "9b. Investigate an environmental issue affecting your community. Share what you learned about that issue with your patrol or troop. Tell what, if anything, could be done by you or your community to address the concern.",
        "9c. On a Scouting or family outing, take note of the trash and garbage you produce. Before your next similar outing, decide how you can reduce, recycle, or repurpose what you take on that outing, and then put those plans into action. Compare your results.",
        "9d. Participate in three hours of service through one or more service projects approved by your Scoutmaster. The project(s) must not be the same service project(s) used for Tenderfoot requirement 7b and Second Class requirement 8e. Explain how your service to others relates to the Scout Law.",
        "10. Tell someone who is eligible to join Scouts BSA, or an inactive Scout, about your Scouting activities. Invite this person to an outing, activity, service project, or meeting. Provide information on how to join, or encourage the inactive Scout to become active. Share your efforts with your Scoutmaster or other adult leader.",
        '11. Demonstrate Scout spirit by living the Scout Oath and Scout Law. Tell how you have done your duty to God and how you have lived four different points of the Scout Law (different from those points used for previous ranks) in your everyday life.',
        "12. While working toward the First Class rank, and after completing Second Class requirement 11, participate in a Scoutmaster conference.",
        "13. Successfully complete your board of review for the First Class rank."),
    "star": (
        "1. Be active in your troop for at least four months as a First Class Scout.",
        "2. As a First Class Scout, demonstrate Scout spirit by living the Scout Oath and Scout Law. Tell how you have done your duty to God and how you have lived the Scout Oath and Scout Law in your everyday life.",
        "3. Earn six merit badges, including any four from the required list for Eagle. You may choose any of the 17 merit badges on the required list for Eagle to fulfill this requirement. See Eagle rank requirement 3 for this list.\n"
        "Name of Merit Badge Date Earned\n"
        "(Eagle-required) _________________________________________\n"
        "(Eagle-required) _________________________________________\n"
        "(Eagle-required) _________________________________________\n"
        "(Eagle-required) _________________________________________\n"
        "_______________________________________________________\n"
        "_______________________________________________________"
        "4. While a First Class Scout, participate in six hours of service through one or more service projects approved by your Scoutmaster.",
        "5. While a First Class Scout, serve actively in your troop for four months in one or more of the following positions of responsibility (or carry out a Scoutmaster-approved leadership project to help the troop): Scout troop. Patrol leader, assistant senior patrol leader, senior patrol leader, troop guide, Order of the Arrow troop representative, den chief, scribe, librarian, historian, quartermaster, bugler, junior assistant Scoutmaster, chaplain aide, instructor, webmaster, or outdoor ethics guide."
        "6. With your parent or guardian, complete the exercises in the pamphlet How to Protect Your Children From Child Abuse: A Parent’s Guide and earn the Cyber Chip award for your grade.",
        "7. While a First Class Scout, participate in a Scoutmaster conference.",
        "8. Successfully complete your board of review for the Star rank."),
    "life": (
        "1. Be active in your troop for at least six months as a Star Scout.",
        "2. As a Star Scout, demonstrate Scout spirit by living the Scout Oath and Scout Law. Tell how you have done your duty to God and how you have lived the Scout Oath and Scout Law in your everyday life.",
        "3. Earn five more merit badges (so that you have 11 in all) including any number more from the list for Eagle so that you have a total of seven from the required list of Eagle in that total number of 11 merit badges. You may choose any of the 17 merit badges on the required list for Eagle to fulfill this requirement. See Eagle rank requirement 3 for this list.\n"
        "Name of Merit Badge Date Earned\n"
        "(Eagle-required) _________________________________________\n"
        "(Eagle-required) _________________________________________\n"
        "(Eagle-required) _________________________________________\n"
        "_______________________________________________________\n"
        "_______________________________________________________"
        "4. While a Star Scout, participate in six hours of service through one or more service projects approved by your Scoutmaster. At least three hours of this service must be conservation-related.",
        "5. While a Star Scout, serve actively in your troop for six months in one or more of the following troop positions of responsibility (or carry out a Scoutmaster-approved leadership project to help the troop).  Scout troop. Patrol leader, assistant senior patrol leader, senior patrol leader, troop guide, Order of the Arrow troop representative, den chief, scribe, librarian, historian, quartermaster, bugler, junior assistant Scoutmaster, chaplain aide, instructor, webmaster, or outdoor ethics guide.",
        "6. While a Star Scout, use the Teaching EDGE method to teach another Scout (preferably younger than you) the skills from ONE of the following choices, so that the Scout is prepared to pass those requirements to their Scoutmaster’s satisfaction.\n"
        "a. Tenderfoot 4a and 4b (first aid)\n"
        "b. Second Class 2b, 2c, and 2d (cooking/tools)\n"
        "c. Second Class 3a and 3d (navigation)\n"
        "d. First Class 3a, 3b, 3c, and 3d (tools)\n"
        "e. First Class 4a and 4b (navigation)\n"
        "f. Second Class 6a and 6b (first aid)\n"
        "g. First Class 7a and 7b (first aid)\n"
        "h. Three requirements from one of the required Eagle merit badges, as approved by your Scoutmaster",
        "7. While a Star Scout, participate in a Scoutmaster conference.",
        "8. Successfully complete your board of review for the Life rank."),
    "eagle": (
        "1. Be active in your troop for at least six months as a Life Scout.",
        "2. As a Life Scout, demonstrate Scout Spirit by living the Scout Oath and Scout Law. Tell how you have done your duty to God, how you have lived the Scout Oath and Scout Law in your everyday life, and how your understanding of the Scout Oath and Scout Law will guide your life in the future. List on your Eagle Scout Rank Application the names of individuals who know you personally and would be willing to provide a recommendation on your behalf, including parents/guardians, religious (if not affiliated with an organized religion, then the parent or guardian provides this reference), educational, employer (if employed), and two other references.",
        "3. Earn a total of 21 merit badges (10 more than required for the Life rank), including these 13 merit badges: (a) First Aid, (b) Citizenship in the Community, (c) Citizenship in the Nation, (d) Citizenship in the World, (e) Communication, (f) Cooking, (g) Personal Fitness, (h) Emergency Preparedness OR Lifesaving, (i) Environmental Science OR Sustainability, (j) Personal Management, (k) Swimming OR Hiking OR Cycling, (l) Camping, and (m) Family Life.  You must choose only one of the merit badges listed in categories i, j, and l. Any additional merit badge(s) earned in those categories may be counted as one of your eight optional merit badges used to make your total of 21.\n"
        "Name of Merit Badge Date Earned \n"
        "1. ____________________________________________________ \n"
        "2. ____________________________________________________\n"
        "3. ____________________________________________________\n"
        "4. ____________________________________________________\n"
        "5. ____________________________________________________\n"
        "6. ____________________________________________________\n"
        "7. ____________________________________________________\n"
        "8. ____________________________________________________\n"
        "9. ____________________________________________________\n"
        "10.____________________________________________________",
        "4. While a Life Scout, serve actively in your troop for six months in one or more of the following positions of responsibility: Scout troop. Patrol leader, assistant senior patrol leader, senior patrol leader, troop guide, Order of the Arrow troop representative, den chief, scribe, librarian, historian, quartermaster, junior assistant Scoutmaster, chaplain aide, instructor, webmaster, or outdoor ethics guide.",
        "5. While a Life Scout, plan, develop, and give leadership to others in a service project helpful to any religious institution, any school, or your community. (The project must benefit an organization other than the Boy Scouts of America.) A project proposal must be approved by the organization benefiting from the effort, your Scoutmaster and unit committee, and the council or district before you start. You must use the Eagle Scout Service Project Workbook, BSA publication No. 512-927, in meeting this requirement. (To learn more about the Eagle Scout service project, see the Guide to Advancement, topics 9.0.2.0 through 9.0.2.16.)",
        "6. While a Life Scout, participate in a Scoutmaster conference.",
        "7. Successfully complete your board of review for the Eagle Scout Rank")}

# Abilities for non-specialized possessions.
# Computer: Allows for online shopping (0 travel time for all stores)
# Cell phone: -25% chance of being late and oversleeping, and an option for recreation.
# Digital Watch: -50% chance of being late and oversleeping.
# Game console: +25% chance of being late and oversleeping, and an option for recreation.
# Camera: +5% chance of being late and oversleeping. Memories saved in game files.
# Full uniform (Pants/Shorts, Shirt, Socks, belt, optional cap) + handbook REQUIRED for troop meetings. If not present, player will be scolded. FUTURE: Will decrease reputation.
"""* SYNCED LIST * means the list of objects associated with this class has one of each item in their respective list above."""


class Statistics:
    """
    Class Statistics
    Creates an object that stores every statistic that the player needs.
    * SYNCED LIST (sort of) *
    """

    def __init__(self, stats=None):
        self.health = self.hunger = self.thirst = self.money = self.reputation = None
        if stats:
            self.health = float(stats[0])
            self.hunger = float(stats[1])
            self.thirst = float(stats[2])
            self.money = float(stats[3])
            self.reputation = int(stats[4])
        else:
            self.health = 100.0
            self.hunger = 50.0
            self.thirst = 50.0
            self.money = 0.0
            self.reputation = 0

    @staticmethod
    def __iter__():
        return ['health', 'hunger', 'thirst', 'money']


class Food:
    """
    Class Food
    Creates an object to store food. Stores the name (str), count (int), fuel (int), and duration (int).
    """

    def __init__(self, name=None, count=None):
        self.name = name if name else None
        match self.name:
            case 'peanuts':
                (self.count, self.fuel, self.duration) = (5, 5, 5)
            case 'breakfast burrito':
                (self.count, self.fuel, self.duration) = (0, 10, 10)
            case 'pancake':
                (self.count, self.fuel, self.duration) = (10, 10, 15)
            case 'mac and cheese':
                (self.count, self.fuel, self.duration) = (0, 20, 30)
            case 'tofu teriyaki':
                (self.count, self.fuel, self.duration) = (0, 30, 35)
            case _:
                (self.count, self.fuel, self.duration) = (0, 0, 0)
        self.count = int(count) if count else self.count

    def __repr__(self):
        return ','.join(str(x) for x in (self.name, self.count, self.fuel, self.duration))

    def __iter__(self):
        return [self.name, self.count, self.fuel, self.duration]


class Drink:
    """
    Class Drink
    Creates an object to store a drink. Stores the name (str), count (int), fuel (int), and duration (int).
    """

    def __init__(self, name=None, count=None):
        self.name = name if name else None
        match self.name:
            case 'water':
                (self.count, self.fuel, self.duration) = (24, 20, 5)
            case 'soda':
                (self.count, self.fuel, self.duration) = (0, 30, 10)
            case 'tea':
                (self.count, self.fuel, self.duration) = (0, 40, 720)
            case _:
                (self.count, self.fuel, self.duration) = (0, 0, 0)
        self.count = int(count) if count else self.count

    def __repr__(self):
        return ','.join(str(x) for x in (self.name, self.count, self.fuel, self.duration))

    def __iter__(self):
        return [self.name, self.count, self.fuel, self.duration]


class Location:
    """
    Class Location
    Creates an object to store a location. Stores the name (str) and distance duration (int).
    * SYNCED LIST *
    """

    def __init__(self, name=None, duration=None):
        self.name = name
        self.duration = int(duration)

    def __repr__(self):
        return self.name + ',' + str(self.duration)


class Chore:
    """
    Class Chore
    Creates an object to store a chore. Stores the name (str) and cooldown status (boolean).
    * SYNCED LIST *
    """

    def __init__(self, name=None, cooldown=False):
        self.name = name
        match self.name:
            case 'unload dishwasher':
                (self.earnings, self.duration) = (5.0, 15)
            case 'load dishwasher':
                (self.earnings, self.duration) = (10.0, 30)
            case 'clean up bedroom':
                (self.earnings, self.duration) = (7.5, 25)
            case 'clean up kitchen':
                (self.earnings, self.duration) = (15, 40)
            case 'clean up dining room':
                (self.earnings, self.duration) = (8.5, 30)
            case 'clean up living room':
                (self.earnings, self.duration) = (7.5, 20)
            case 'collect the trash':
                (self.earnings, self.duration) = (10.0, 10)
        self.cooldown = cooldown == "True"

    def __repr__(self):
        return self.name + ',' + str(self.cooldown)


class Possession:
    """
    Class Possession
    Creates an object to store a possession. Stores the name (str) and attempts to execute the specific attribute.
    * SYNCED LIST *
    """

    def __init__(self, name=None):
        self.name = name
        try:
            exec(possession_attributes[name])
        except (KeyError, IndexError):
            pass

    def __repr__(self):
        return self.name


class Event:
    """
    Class Event.
    Creates an object to store an event. Stores the name (str), date (datetime object), and importance (int)
    """

    def __init__(self, name=None, date=None, importance=None):
        self.name = name
        if "datetime" in date.__repr__():
            self.date = date
        else:
            self.date = dt.strptime(date, '%m%d%Y%H%M')
        self.importance = importance

    def __repr__(self):
        return self.name + ',' + self.date.strftime('%m%d%Y%H%M') + ',' + str(self.importance)

    def alert_message(self):
        """
        Method to summarize the event.
        :return: Name, readable date and time, and importance.
        """
        return "EVENT: {} on {} at {}. Importance: {}".format(self.name, self.date.strftime("%m/%d/%y"), self.date.strftime("%H:%M"), self.importance)


class Rank:
    """
    Class Rank.
    Creates an object to store a rank. Stores the name (str) and a list of its respective requirements (Requirement).
    * Requirements are SYNCED *
    """

    def __init__(self, rank, info):
        self.rank = rank
        self.requirement_list = [Requirement(i, (info[ranks[rank].index(i)] if info else False)) for i in ranks[rank]]

    def __repr__(self):
        return self.rank + '\t' + ','.join([str(i.status) for i in self.requirement_list])


class Requirement:
    """
    Class Requirement.
    Creates an object to store a requirement. Stores the name (str) and the completion status (boolean).
    """

    def __init__(self, name, status=None):
        self.name = name
        self.status = status == "True" if status else False

    def __repr__(self):
        return self.status.upper() + '\t' + self.name


class ScoutRPG:
    """
    Class ScoutRPG.
    Houses all the methods pertaining to the main game. This is the good stuff.
    """
    category = "games"
    version = 'alpha1.5'
    sleep_weight = [0, 0, 1, 1, 1, 2, 3, 3, 3, 3, 4, 4, 4]
    choices = {'self.eat()': "eat", 'self.drink()': "drink", 'self.sleep()': "sleep", 'self.heal()': "heal",
               'self.house_chores()': "chores", 'self.travel()': "travel", 'self.agenda()': "agenda", 'self.show_rank()': "rank"}
    memories = False
    online_shopping = False

    @staticmethod
    def boot(path='\\'):
        """
        This method regulates the bootup sequence of the game and helps it connect to Cerberus
        :param path: Path for game files.
        :return: Nothing.
        """
        scout_rpg = ScoutRPG(path)
        if not scout_rpg.filename == "exit":
            scout_rpg.main()
        return

    def __init__(self, path):
        # Default game setup code, pulled from sonar.py.
        self.new_file = False
        self.filename = ""
        self.path = path
        game_info = bagels.init_game(self, path, 'sct')
        # Default stats for the time being. Health, Hunger, Thirst, and time (date, hour, minute).
        if game_info:
            # Decrypting everything and cutting off the new line at the end!
            try:
                version = Loading.caesar_decrypt(game_info[0]).split('\n')[0]
                # UPDATE Add versions here after updates!!!
                if version not in ("prealpha", "alpha1.0", "alpha1.1", "alpha1.2", "alpha1.3", "alpha1.4", "alpha1.4.1", "alpha1.5", "alpha1.6"):
                    raise IndexError
            except IndexError:
                if input("There is no version in the selected game file. Type ENTER to delete it, or stop the program now "
                         "to attempt to recover progress by yourself.") == "ENTER":
                    os.remove(self.path + '\\' + self.filename)
                return
            try:
                # Checking for update and unpacking...
                (version, stats, food, drinks, game_time, locations, chores, possessions, events, rank) = self.update_check(version, [Loading.caesar_decrypt(i).split('\n')[0] for i in game_info])
                # stats will look something like "100.0\t50.0\t50.0\t0.0"
                self.stats = Statistics(stats.split('\t')) if stats else Statistics()
                # Food data looks like peanuts,5,5,5\tpancake10,10,15
                self.food = [Food(i.split(',')[0], i.split(',')[1]) for i in food.split('\t')] if food else []
                self.drinks = [Drink(i.split(',')[0], i.split(',')[1]) for i in drinks.split('\t')] if drinks else []
                self.locations = [Location(i.split(',')[0], i.split(',')[1]) for i in locations.split('\t')] if locations else []
                self.time = dt.strptime(game_time, "%m%d%Y%H%M") if game_time else None
                self.difference = [0, 0, 0, 0]
                self.chores = [Chore(i.split(',')[0], i.split(',')[1]) for i in chores.split('\t')] if chores else []
                self.possessions = [Possession(i) for i in possessions.split('\t')] if possessions else []
                self.events = [Event(i.split(',')[0], i.split(',')[1], i.split(',')[2]) for i in events.split('\t')] if events else []
                self.rank = Rank(rank.split('\t')[0], rank.split('\t')[1].split(',')) if rank else Rank("scout", [])
            except (KeyError, IndexError, ValueError):
                # If the element doesn't exist.
                if input("This game save is corrupted! Nooooo...\nType ENTER to delete it, or stop the program now "
                         "to attempt to recover progress by yourself.") == "ENTER":
                    os.remove(self.path + '\\' + self.filename)
                return
        return

    def quit(self):
        """
        Regulates the rewriting of game files and quitting the game.
        :return: Nothing.
        """
        if self.new_file:
            self.filename = input("File name?\n") + '.sct'
        stats = '\t'.join(str(self.stats.__getattribute__(i)) for i in self.stats.__iter__()) + '\t' + str(self.stats.reputation)
        food = '\t'.join(i.__repr__() for i in self.food)
        drinks = '\t'.join(i.__repr__() for i in self.drinks)
        game_time = self.time.strftime("%m%d%Y%H%M")
        locations = '\t'.join(i.__repr__() for i in self.locations)
        chores = '\t'.join(i.__repr__() for i in self.chores)
        possessions = '\t'.join(i.__repr__() for i in self.possessions)
        events = '\t'.join(i.__repr__() for i in self.events)
        rank = self.rank.__repr__()
        try:
            game = open(self.path + '\\' + self.filename, 'w')
            for i in (ScoutRPG.version, stats, food, drinks, game_time, locations, chores, possessions, events, rank):
                game.write(Loading.caesar_encrypt(i) + '\n')
            game.close()
        except (FileNotFoundError, FileExistsError):
            Loading.returning("The path or file was not found.", 2)
        Loading.returning("Saving game progress...", 2)
        return

    def refresh(self, element=None, value=None):
        """
        Updates the clock. Can add time or simply update it
        :param element: Specifies what element of time to add
        :param value: Specifies how much of element to add
        :return: Code 0 if player doesn't want to try again, and Code 1 if they do
        """
        previous_time = self.time
        # Check if we're modifying time or updating it.
        if element and value:
            # Make sure the passed element is ok.
            if element in ("day", "hour", "minute"):
                self.time += td(days=value if element == "day" else 0,
                                hours=value if element == "hour" else 0,
                                minutes=value if element == "minute" else 0)
            # Math to calculate total time.
            self.difference[0] += abs(self.time - previous_time).total_seconds()
            self.difference[1] += abs(self.time - previous_time).total_seconds()
            if self.difference[0] >= 3600:
                self.stats.hunger -= 5 * (self.difference[0] / 3600)
                self.difference[0] = 0
            if self.difference[1] >= 1800:
                self.stats.thirst -= 5 * (self.difference[1] / 1800)
                self.difference[1] = 0
            if self.stats.hunger <= 0:
                self.difference[2] += (3600 * (abs(self.stats.hunger) / 600))
            if self.stats.thirst <= 0:
                self.difference[3] += (1800 * (abs(self.stats.thirst) / 300))
            if self.stats.hunger <= 0 and self.difference[2] >= 600:
                self.stats.health -= 1 * (self.difference[2] / 600)
                self.difference[2] = 0
            if self.stats.thirst <= 0 and self.difference[3] >= 300:
                self.stats.health -= 1 * (self.difference[3] / 300)
                self.difference[3] = 0
        else:
            # Capping each stat to 0 or 100.
            for i in self.stats.__iter__():
                if i != "money":
                    self.stats.__setattr__(i, 0.0) if self.stats.__getattribute__(i) < 0.0 else self.stats.__getattribute__(i)
                    self.stats.__setattr__(i, 100.0) if self.stats.__getattribute__(i) > 100.0 else self.stats.__getattribute__(i)
                    self.stats.__setattr__(i, round(self.stats.__getattribute__(i), 1))
            self.stats.money = round(self.stats.money, 2)
            # Some easter eggs :)
            if self.stats.money >= 1000000000000:
                Loading.returning("Ok, we get it. You're a trillionaire in a Boy Scouting Simulator.")
            if self.stats.money >= 1000000000001:
                Loading.returning("Ok, that's not right... You can't be a trillionaire in this game!")
                self.stats.__setattr__("money", 1000)
            if self.stats.money < 0:
                Loading.returning("Wait, you can't be in debt in this game! Here's some free money.")
                self.stats.__setattr__("money", 10)
            # 1 Hour reminder for events!
            for i in self.events:
                if 0 > (self.time - i.date).total_seconds() > -3600:
                    Loading.returning("Less than one hour until {}!".format(i.name), 3)
                if (self.time - i.date).total_seconds() == 0:
                    try:
                        exec(event_list[i.name.lower()])
                    except KeyError:
                        pass
                # Adding the weekly troop meeting.
                if self.time.weekday() == 0 and sum([i.name == "Troop Meeting" for i in self.events]) < 0:
                    troop_meeting = Event("Troop Meeting", self.time.month + str(int(self.time.day) + 1) + self.time.year + '1900', 3)
                    self.events.append(troop_meeting)
                    Loading.returning(troop_meeting.alert_message())
        # Daily stuff
        if self.time.day > previous_time.day:
            for i in self.chores:
                i.__setattr__('cooldown', False)
            self.stats.money += 25
            Loading.returning("ALLOWANCE: $25.00 has been added to your wallet.", 2)
        if self.stats.health <= 0.0:
            if self.defeat() == 1:
                self.setup()
            else:
                return 1
        return

    def update_check(self, version, datapack):
        """
        Checks the game file for an update.
        Checks the version of the game file against multiple options and updates the file recursively (sort of). The version is redefined as the next version, so that the next check works. Then the next check runs and does it again
        :param version: This is the version of the game file
        :param datapack: This is the variable to unpack all the game file data
        :return: Returns the updated data pack.
        """
        # "Recursive" method to upgrade game files saved in previous versions.
        if version == 'prealpha':
            # Adding money, locations, chores, possessions, and renaming food and drinks.
            version = 'alpha1.0'
            (stats, food, drinks, game_time) = datapack[1:]
            stats = '\t'.join(stats.split(',')) + '\t0.0'
            food = food.split('\t')
            for i in range(len(food)):
                match food[i].split(',')[2]:
                    case '5':
                        food[i] = 'peanuts,' + food[i]
                    case '10':
                        food[i] = 'breakfast burrito,' + food[i]
                    case '15':
                        food[i] = 'pancake,' + food[i]
                    case '30':
                        food[i] = 'mac and cheese,' + food[i]
                    case '35':
                        food[i] = 'tofu teriyaki,' + food[i]
            food = '\t'.join(food)
            drinks = drinks.split('\t')
            for i in range(len(drinks)):
                match drinks[i].split(',')[2]:
                    case '5':
                        drinks[i] = 'water,' + drinks[i]
                    case '10':
                        drinks[i] = 'soda,' + drinks[i]
            drinks = '\t'.join(drinks)
            locations = 'grocery store,10\tdepartment store,20\tscout store,30'
            chores = '\t'.join(i + ',False' for i in chore_list)
            possessions = ''
            datapack = [version, stats, food, drinks, game_time, locations, chores, possessions]
        if version == 'alpha1.0':
            # Filtering removed possessions.
            version = 'alpha1.1'
            (stats, food, drinks, game_time, locations, chores, possessions) = datapack[1:]
            if possessions:
                possessions = possessions.split('\t')
                for i in range(len(possessions)):
                    (name, quantity) = possessions[i].split(',')
                    possessions[i] = '\t'.join([name] * int(quantity))
                possessions = '\t'.join(possessions)
            datapack = [version, stats, food, drinks, game_time, locations, chores, possessions]
        if version == 'alpha1.1':
            # Adding the day to the time.
            version = 'alpha1.2'
            (stats, food, drinks, game_time, locations, chores, possessions) = datapack[1:]
            game_time = game_time.split(',')
            game_time = [list(calendar.day_name)[dt.strptime('{} {} {}'.format(game_time[0], game_time[1], game_time[2]), '%m %d %Y').weekday()]] + game_time
            game_time = ','.join(game_time)
            datapack = [version, stats, food, drinks, game_time, locations, chores, possessions, '']
        if version == 'alpha1.2':
            # Changing from list to datetime object.
            version = 'alpha1.3'
            (stats, food, drinks, game_time, locations, chores, possessions, events) = datapack[1:]
            game_time = game_time.split(',')
            game_time = game_time[1] + game_time[2] + game_time[3] + game_time[4] + game_time[5]
            new_possessions = []
            if possessions:
                possessions = possessions.split('\t')
                for i in range(len(possessions)):
                    if possessions[i] not in ("reusable plastic box", "reusable liquid flask", "kitchen cabinets", "refrigerator"):
                        new_possessions.append(possessions[i])
            new_possessions = '\t'.join(new_possessions)
            datapack = [version, stats, food, drinks, game_time, locations, chores, new_possessions, events]
        if version == 'alpha1.3' or version == 'alpha1.4':
            # Adding Reputation.
            version = 'alpha1.4.1'
            (stats, food, drinks, game_time, locations, chores, possessions, events) = datapack[1:]
            stats += '\t0'
            datapack = [version, stats, food, drinks, game_time, locations, chores, possessions, events]
        if version == 'alpha1.4.1':
            # Adding Rank.
            version = ScoutRPG.version
            (stats, food, drinks, game_time, locations, chores, possessions, events) = datapack[1:]
            rank = ("scout\t" + ','.join([str(False)] * len(ranks["scout"])))
            datapack = [version, stats, food, drinks, game_time, locations, chores, possessions, events, rank]
            # Now to quit and rewrite the game files.
            # UPDATE THIS SHOULD BE MOVED TO THE BOTTOM OF THE UPGRADE TREE!
            file = open(self.path + '\\' + self.filename, 'w')
            for i in datapack:
                file.write(Loading.caesar_encrypt(i) + '\n')
            file.close()
            Loading.returning("This game was saved in an older version of ScoutRPG. The save file will now be updated.", 3)
        return datapack

    def main(self):
        """
        Main method loop for gameplay.
        :return: Nothing.
        """
        # Setup logic
        if self.new_file:
            self.setup()
        while True:
            if self.refresh() == 1:
                return
            # Status report. Date, time, all stats.
            print(self.time.strftime("\nDate: %A, %m/%d/%Y\nTime: %H:%M"))
            print('\n'.join(i + (": $" if i == "Money" else ": ") + str(self.stats.__getattribute__(i.lower())) for i in stats_list))
            print("Rank: " + self.rank.rank.capitalize())
            action = input('What would you like to do? Type "help" for help').lower()
            if action == "help":
                input('Here is a list of common actions:\n1. Eat\n2. Drink\n3. Sleep\n4. Heal\n5. Chores\n6. Travel\n7. Agenda\n8. Rank'
                      'You can type "exit" to exit')
            if action in ('quit', 'exit', 'leave', 'save'):
                self.quit()
                return
            for i in ScoutRPG.choices:
                if action == ScoutRPG.choices[i]:
                    print()
                    exec(i)
                    break

    def setup(self):
        """
        Setup method to set all variables up for a new game.
        :return: Nothing.
        """
        if 'yes' in input("Would you like to view the premise?").lower():
            input("Welcome to Scouting!\nYou have embarked on a journey far beyond any other. Your physical and mental skills "
                  "will be tested. Your memory will be trained. Your survival instinct will be brought to life.\nPress ENTER "
                  "to continue.")
            input("\nYou are a boy scout, fresh out of cub scouts and ready to start your journey to Eagle. You need to show that you "
                  "are worthy of this rank by going to meetings, outings, camping trips, conferences, and service projects. These "
                  "are all events you can do to advance yourself.\nPress ENTER to continue.")
            input("\nYou have 6 main statistics: Health, Hunger, Thirst, Money, Agenda, and Rank.\nHEALTH is your body health. It can "
                  "be influenced by hunger, thirst, injuries, and first aid kits.\nHUNGER is how hungry you are. It can be influenced "
                  "by food.\nTHIRST is how thirsty you are. It can be influenced by beverages.\nMONEY is how much money you have. You "
                  "can do chores to get money, but you need money to buy things as well.\nAGENDA is your schedule for the day. It will "
                  "include events that you signed up for and should attend.\nRANK is your current Boy Scout Rank. The ranks are (in "
                  "order): Scout, Tenderfoot, Second Class, First Class, Star, Life, Eagle.\nPress ENTER to continue.")
            input("Your ultimate goal is to reach Eagle Scout and you have 7 years to do it. You are 11 years old, and you age out "
                  "at 18 years old. Good luck!")
        home = input("Would you like your home to be closer to the grocery store, department store, or scout store? "
                     "\nThe default is closer to the grocery store")
        if home in ("department", "department store"):
            self.locations = ("department store", "scout store", "grocery store")
        elif home in ("scout", "scout store"):
            self.locations = ("scout store", "grocery store", "department store")
        else:
            self.locations = ("grocery store", "department store", "scout store")
        self.stats = Statistics()
        self.food = [Food(i) for i in ("peanuts", "pancake")]
        self.drinks = [Drink("water")]
        self.time = dt.strptime("0301" + str(dt.today().year) + "0800", "%m%d%Y%H%M")
        self.difference = [0, 0, 0, 0]
        self.locations = [Location(i, 10 * (self.locations.index(i) + 1)) for i in self.locations]
        self.chores = [Chore(i) for i in chore_list]
        self.possessions = []
        self.events = []
        self.rank = Rank("scout", [])
        return

    def eat(self):
        """
        Method to EAT THINGS
        :return: Nothing.
        """
        print("Here's the food you have:")
        print('\n'.join("{} {} meals".format(str(i.count).title(), i.name) for i in self.food if i.count > 0))
        while True:
            action = input("What would you like to eat?").lower()
            if not action:
                return
            try:
                action = [i for i in self.food if i.name == action][0]
                # Correctly remove 1, add hunger, and add time.
                action.count -= 1
                self.stats.hunger += action.fuel
                self.refresh("minute", action.duration)
                Loading.returning("You eat a {} meal, and it was {}".format(action.name.title(), ["tasty", "delicious", "scrumptious"][random.randint(0, 2)]), 2)
                if action.count <= 0:
                    self.food.pop(self.food.index(action))
                break
            except (IndexError, ValueError):
                Loading.returning("You don't have any {} meals!".format(action), 2)
        return

    def drink(self):
        """
        Method to DRINK THINGS
        :return: Nothing.
        """
        print("Here are the beverages you have:")
        print('\n'.join("{} bottles of {}".format(str(i.count).title(), i.name) for i in self.drinks if i.count > 0))
        while True:
            action = input("What would you like to drink?").lower()
            if not action:
                return
            try:
                action = [i for i in self.drinks if i.name == action][0]
                # Correctly remove 1, add hunger, and add time.
                action.count -= 1
                self.stats.thirst += action.fuel
                self.refresh("minute", action.duration)
                Loading.returning("You drink a bottle of {}, and it was {}".format(action.name.title(), ["quenching", "tasty", "refreshing"][random.randint(0, 2)]), 2)
                if action.count <= 0:
                    self.drinks.pop(self.drinks.index(action))
                break
            except (IndexError, ValueError):
                Loading.returning("You do not have any bottles of {}!".format(action), 2)
        return

    def sleep(self):
        """
        Method to SLEEP
        :return: Nothing
        """
        if 8 >= int(self.time.hour) >= 21:
            self.refresh("day", 1)
            self.time = self.time.replace(hour=8, minute=00)
            self.stats.hunger = 25 if self.stats.hunger > 25 else self.stats.hunger
            self.stats.thirst = 25 if self.stats.thirst > 25 else self.stats.thirst
            print("SLEEP: Until 8:00")
            Loading.returning("It's getting late, so you turn in for the day.", 3)
            Loading.returning("Zzzzzzz...", 3)
        else:
            sleep_time = ScoutRPG.sleep_weight[random.randint(0, len(ScoutRPG.sleep_weight) - 1)]
            if self.stats.hunger <= 0 or self.stats.thirst <= 0:
                Loading.returning("ALERT: Your Health is getting low. Eat or drink something after you sleep.", 3)
            match sleep_time:
                case 0:
                    self.refresh("minute", 30)
                    print("SLEEP: 30 Minutes")
                    Loading.returning("You take a small nap and feel more energized.", 3)
                case 1:
                    self.refresh("hour", 1)
                    print("SLEEP: 1 Hour")
                    Loading.returning("You take a good nap and are ready to progress.", 3)
                case 2:
                    self.refresh("hour", 2)
                    print("SLEEP: 2 Hours")
                    Loading.returning("You sleep for a while after your alarm, but you still have time in the day.", 3)
                case 3:
                    self.refresh("hour", 3)
                    print("SLEEP: 3 Hours")
                    Loading.returning("You oversleep a little bit, but it's nothing special.", 3)
                case 4:
                    self.refresh("hour", 4)
                    print("SLEEP: 4 Hours")
                    Loading.returning("Oops! You oversleep a lot and are quite hungry.", 3)
        return

    def heal(self):
        """
        Method to HEAL the player back up to 100.
        :return: Nothing.
        """
        if self.stats.health < 100.0:
            self.stats.health = 100.0
            Loading.returning("You use a small first aid kit, food, and water to replenish yourself.", 3)
            Loading.returning("Make sure to eat and drink regularly!", 2)
        else:
            Loading.returning("You don't need to heal!", 2)
        return

    def house_chores(self):
        """
        Method to do chores and earn money.
        :return: Nothing.
        """
        print('\n'.join(str(i.name.title()) + " - +$" + str(i.earnings) + ' --> ' + str(i.duration) + ' minutes' + (", READY" if not i.cooldown else '') for i in self.chores))
        while True:
            action = input("Which chore do you want to do?")
            if not action:
                return
            elif action in chore_list:
                action = [i for i in self.chores if i.name == action][0]
                if not action.cooldown:
                    action.__setattr__('cooldown', True)
                    Loading.progress_bar(action.name.title().split(' ', 1)[0] + 'ing ' + action.name.title().split(' ', 1)[1], action.duration / 4)
                    self.stats.money += action.earnings
                    self.refresh("minute", action.duration)
                    Loading.returning("Chore complete! ${}0 has been added to your wallet. You may not do this chore again today.".format(action.earnings), 3)
                    return
                else:
                    Loading.returning("You have already done that chore today!", 2)
            else:
                Loading.returning("Please enter a valid chore or press ENTER to return.", 2)

    def travel(self):
        """
        Method to travel to other destinations.
        :return: Nothing.
        """
        stores = (self.groceries, self.department, self.scout_store)
        if ScoutRPG.online_shopping:
            print("You have a computer! Welcome to Online Shopping.\nType the store you want to buy from.")
            print('\n'.join(str(i.name.title()) + ' --> 0 minutes' for i in self.locations))
            destination = input("Where would you like to go?").lower()
            destination = destination + " store" if "store" not in destination else destination
            for i in self.locations:
                if destination == i.name:
                    Loading.progress_bar("www.{}.com".format(i.name.lower().replace(' ', '_')), 0.0001)
                    stores[locations_list.index(i.name)]()
        else:
            print('\n'.join(str(i.name.title()) + ' --> ' + str(i.duration) + ' minutes' for i in self.locations))
            destination = input("Where would you like to go?").lower()
            destination = destination + " store" if "store" not in destination else destination
            for i in self.locations:
                if destination == i.name:
                    self.refresh("minute", i.duration)
                    Loading.progress_bar("Traveling to the {}...".format(destination), i.duration / 4)
                    stores[locations_list.index(i.name)]()
                    Loading.progress_bar("Traveling back home...".format(destination), i.duration / 4)
                    self.refresh("minute", i.duration)
                    break
            else:
                Loading.returning("Please pick a valid destination.", 2)
        return

    def groceries(self):
        """
        Method for buying Groceries (Foods and Drinks)
        :return: Nothing.
        """
        print("\n\nWelcome to the grocery store!")
        Loading.returning("Here you can buy food and drinks.", 2)
        print('\nFOOD')
        print('\n'.join(str(food_list.index(food_list[i]) + 1) + '. ' + food_list[i].title() + ' - $' + str(food_costs[i]) for i in range(len(food_list))))
        print('\nDRINKS')
        print('\n'.join(str(drinks_list.index(drinks_list[i]) + 1) + '. ' + drinks_list[i].title() + ' - $' + str(drinks_cost[i]) for i in range(len(drinks_list))))
        while True:
            print("Wallet: ${}0".format(self.stats.money))
            buy = input('What would you like to buy? Type "exit" to exit.').lower()
            if buy == 'exit':
                return
            elif buy in food_list:
                if self.buy(buy, self.food, food_list, food_costs, Food) == 0:
                    break
            elif buy in drinks_list:
                if self.buy(buy, self.drinks, drinks_list, drinks_cost, Drink) == 0:
                    break
            else:
                Loading.returning("Please type a valid food/drink.")
        return

    def department(self):
        """
        Method to buy departmental possessions.
        :return: Nothing.
        """
        print("\n\nWelcome to the Department store!")
        Loading.returning("Here you can buy various utilities to add to your lifestyle.", 3)
        print("\nOUTDOORS")
        print('\n'.join(str(department_list.index(i) + 1) + '. ' + i.title() + ': $' + str(department_costs[department_list.index(i)]) for i in department_list[0:6]))
        print("\nELECTRONICS")
        print('\n'.join(str(department_list.index(i) - 2) + '. ' + i.title() + ': $' + str(department_costs[department_list.index(i)]) for i in department_list[6:]))
        while True:
            print("Wallet: ${}0".format(self.stats.money))
            buy = input('What would you like to buy? Type "exit" to exit.').lower()
            if buy == 'exit':
                return
            elif buy in department_list:
                if self.buy(buy, self.possessions, department_list, department_costs, Possession) == 0:
                    break
            else:
                Loading.returning("Please type a valid item.")
        # Buy Utilities. Everything bought here is stored as objects in a list: self.possessions.
        # Desk: $50 - Reduces time needed to study for ranks.
        # Reusable Plastic Box: $25 - +5 food space.
        # Reusable Liquid Flask: $25 - +5 drinks space
        # Computer: $450 - Reduces time to study for ranks + Ability to purchase things online! - ONE TIME
        # Kitchen Cabinets: $350 - +20 Food space, +10 Drinks space - ONE TIME
        # Refrigerator: $550 - +15 drinks space, +10 food space - ONE TIME
        return

    def scout_store(self):
        """
        Method to buy Scout possessions.
        :return: Nothing.
        """
        exec("print('\nWelcome to the Scout Store!') ; Loading.returning('Here you can buy your various scouting equipment.', 2) ; print('\nSCOUT-BRANDED CLOTHING')")
        i = 0
        while i < 10:
            print("{}. {}: ${}".format(i + 1, scout_store_list[i].title(), scout_store_costs[i]) + ('\t' * int(math.ceil((20 - len(scout_store_list[i])) / 4))) + "{}. {}: ${}".format(i + 2, scout_store_list[i + 1].title(), scout_store_costs[i + 1]))
            i += 2
        exec('print("{}. {}: ${}".format(11, scout_store_list[10].title(), scout_store_costs[10])) ; i+= 1 ; print("\nOUTDOORS")')
        # print('\n'.join(str(scout_store_list.index(i) + 1) + '. ' + i.title() + ': $' + str(scout_store_costs[scout_store_list.index(i)]) for i in scout_store_list[0:11]))
        while 10 < i < 24:
            print("{}. {}: ${}".format(i - 10, scout_store_list[i].title(), scout_store_costs[i]) + ('\t' * int(((24 - len(scout_store_list[i])) / 4))) + "{}. {}: ${}".format(i - 9, scout_store_list[i + 1].title(), scout_store_costs[i + 1]))
            i += 2
        print("{}. {}: ${}".format(15, scout_store_list[25].title(), scout_store_costs[25]))
        # print('\n'.join(str(i - 10) + '. ' + scout_store_list[i].title() + ': $' + str(scout_store_costs[i]) for i in range(len(scout_store_list))[11:]))
        while True:
            print("Wallet: ${}0".format(self.stats.money))
            buy = input('What would you like to buy? Type "exit" to exit.').lower()
            if buy == 'exit':
                return
            elif buy in scout_store_list:
                if self.buy(buy, self.possessions, scout_store_list, scout_store_costs, Possession) == 0:
                    break
            else:
                Loading.returning("Please type a valid item.")
        return

    def buy(self, buy, stat, store_list, store_costs, item):
        """
        Universal method to buy things
        :param buy: What the player wants to buy
        :param stat: List to add objects to
        :param store_list: List to check buy against
        :param store_costs: List to get costs from
        :param item: Object type to add
        :return: Nothing.
        """
        while True:
            quantity = input('How many {} would you like? Type "exit" to exit.'.format(buy))
            if quantity == 'exit':
                return
            else:
                try:
                    quantity = int(quantity)
                except (TypeError, ValueError):
                    Loading.returning("Please type a number between 0 and 100.", 2)
                    continue
            if 0 <= quantity <= 100.0:
                if self.stats.money >= (quantity * store_costs[store_list.index(buy)]):
                    self.stats.money -= (quantity * store_costs[store_list.index(buy)])
                    try:
                        stat[[stat.index(i) for i in stat if i.name == buy][0]].count += quantity
                    except IndexError:
                        stat.append(item(buy))
                        stat[[stat.index(i) for i in stat if i.name == buy][0]].count = quantity
                    Loading.returning("Purchase successful. Your total was: ${}0".format(str(quantity * store_costs[store_list.index(buy)])), 2)
                    return
                else:
                    Loading.returning("You don't have enough money! ({})".format(self.stats.money), 2)
                    break
            else:
                Loading.returning("Please type a number between 0 and 100.", 2)
        return

    def agenda(self):
        """
        Method to show current events.
        :return: Nothing.
        """
        print('\n'.join([i.name + " on " + i.date.strftime("%A, %m/%d/%Y at %H:%M") + ". Importance: " + str(i.importance) for i in self.events]) if self.events else "No events.")
        print(self.time.strftime("\nToday's date: %B %d, %Y\n") + calendar.TextCalendar(6).formatmonth(int(self.time.year), int(self.time.month)))
        if input('Type "add event" to add a custom event or Press ENTER to continue.') == 'add event':
            self.events.append(Event(input("What is the event name?"), input("Date and time of the event? E.g. 030120221900"), int(input("Importance of the event?"))))
        return

    def troop_meeting(self):
        """
        Method to simulate a Troop Meeting.
        :return: Nothing.
        """

        class MeetingEvent:
            """
            Class MeetingEvent.
            Creates an object that stores a MeetingEvent. This is an event specific to a Troop meeting that only happens here.
            Stores the name, response for typing Yes, response for typing No, the reputation associated, and the follow-up messages for typing yes or no.
            """

            def __init__(self, event, yes_msg, no_msg, reputation, follow_up_yes, follow_up_no):
                self.event = event
                self.yes_msg = yes_msg
                self.no_msg = no_msg
                self.reputation = reputation
                self.follow_up_yes = follow_up_yes
                self.follow_up_no = follow_up_no
                self.answer = None

        Loading.returning("Welcome to the troop meeting.", 2)
        required_uniform = ["shirt", "pants", "socks", "belt", "neckerchief", "slide", "shoes"]
        for i in self.possessions:
            for j in required_uniform:
                if j in i.name:
                    required_uniform.pop(required_uniform.index(j))
                    break
        if required_uniform:
            Loading.returning(["Your Scoutmaster was outside the door ", "An adult leader saw you walk in ", "Your friend was at your table "][random.randint(0, 2)] +
                              ["and noticed you didn't have your ", "and commented on your lack of ", "and scolded you for not having your "][random.randint(0, 2)] +
                              ', '.join(required_uniform) + '. Make sure you have it next meeting! -{} Reputation'.format(5 * len(required_uniform)), 5)
            self.stats.reputation -= 5 * len(required_uniform)

        Loading.returning("The flag ceremony has begun.", 2)
        for i in ('"Color Guard, Attention!"', '"Troop, Attention!"', '"Color Guard, forward march!"', '"Color Guard, halt!"',
                  '"Color Guard, prepare to post the colors!"', '"Scout hand salute!"', '"Please join me in the pledge of allegiance."',
                  '"I pledge allegiance to the flag of the United States of America. And to the Republic, for which it stands, '
                  'one nation, under God, indivisible, with Liberty and Justice for all."', '"Color Guard, Post the colors!"', '"Two!"    ',
                  '"Color Guard, about... face!"', '"Color Guard, reform!"', '"Color Guard, forward march!"', '"Color Guard, dismissed! Troop, at ease."'):
            Loading.returning(i, int(len(i) / 10))
        Loading.returning("The flag ceremony has ended.", 2)
        Loading.returning("You head to your table and sit down.", 2)
        events = []
        for i in random.sample(
                [MeetingEvent(i[0], i[1], i[2], i[3], i[4], i[5]) for i in [("A friend approaches you and asks for your help. Yes or no?", "Your friend appreciates the help. He may ask you later.", "Your friend woefully walks away. He may ask you later.",
                                                                             5, "The same friend has returned, asking for more help. Yes or no?", "The same friend has returned, but glares at you and walks away."),
                                                                            ("A surprise uniform inspection has occurred!", "", "", 0, "", ""),
                                                                            ("Your patrol wants to organize an outing. Yes or no?", "Your patrol is grateful for your support.", "Your patrol scoffs at your laziness and continues their planning", 15,
                                                                             "Your patrol has finalized the event and is asking your attendance. Yes or no?", "Your patrol now wants to organize a fun outing after your display of laziness. Yes or no?"),
                                                                            ("The scoutmaster is asking you if the meeting is going well. Yes or no?", "The scoutmaster is glad you enjoy the meeting.", "The scoutmaster is sorry you aren't having fun.", 10,
                                                                             "", ""),
                                                                            ("You see your friend playing on his phone and think about telling him to stop. Yes or no?",
                                                                             "Your friend scoffs at you and puts it away. An adult leader comes by later, and your friend thanks you for the advice.",
                                                                             "Your friend continues to play and an adult leader comes by. They scold your friend and take away his phone.", 5,
                                                                             "Your friend pulls his phone out again, but looks at you and puts it away.", "The adult leader comes back with your friend's phone and gives him a stern talk."),
                                                                            ("The weekly meeting game has begun. Are you going to participate? Yes or no?", ("The game goes well. Your team wins and you are glad you participated.",
                                                                                                                                                             "The game goes awry. Your team loses but you are glad you participated.")[random.randint(0, 1)],
                                                                             "The game goes well, and everyone has fun. Everyone except you.", 20, "", ""),
                                                                            ("You had a long day today and you are just about to fall asleep. Slap yourself awake? Yes or no?",
                                                                             "You slap yourself and your patrol looks at you. You explain it and they understand.",
                                                                             "You fall asleep and have a good dream. Thankfully, your patrol notices and wake you up before a leader comes by.", 10,
                                                                             "You almost fall asleep again when your patrol wakes you up.",
                                                                             "You fall asleep again but your patrol rolls their eyes and you later get scolded by a leader."),
                                                                            ("Your friend is going for a scoutmaster conference and asks for good luck. Yes or no?", "He thanks you for your wishes and heads off, feeling confident.",
                                                                             "Your friend walks away annoyed at you.", 5, "Your friend returns from the conference with a happy face and thanks you for the confidence.",
                                                                             "Your friend comes back from the conference and looks down the whole time. He gives you a glare before walking away.")]], 3):
            if "Yes or no" in i.event:
                for j in range(3):
                    print(i.event)
                    choice = input().lower()
                    if "yes" in choice:
                        exec("Loading.returning(i.yes_msg + ' +{} Reputation.'.format(i.reputation), 3) ; self.stats.reputation += i.reputation ; i.answer = True ; events.append(i)")
                        break
                    elif "no" in choice:
                        exec("Loading.returning(i.no_msg + ' -{} Reputation.'.format(i.reputation), 3) ; self.stats.reputation -= i.reputation ; i.answer = False ; events.append(i)")
                        break
                    else:
                        Loading.returning("Invalid response. {} attempts remaining. Please try again.".format(2 - j), 2)
                else:
                    Loading.returning("3 attempts exceeded. Moving on... +0 Reputation", 3)
            else:
                Loading.returning(i.event, 3)
        random.shuffle(events)
        for i in events:
            follow_up = i.follow_up_yes if i.answer else i.follow_up_no
            if follow_up:
                if "Yes or no" in follow_up:
                    for j in range(3):
                        print(follow_up)
                        choice = input().lower()
                        if "yes" in choice:
                            exec("Loading.returning(i.yes_msg + ' +{} Reputation.'.format(i.reputation), 3) ; self.stats.reputation += i.reputation")
                            break
                        elif "no" in choice:
                            exec("Loading.returning(i.no_msg + ' -{} Reputation.'.format(i.reputation), 3) ; self.stats.reputation -= i.reputation")
                            break
                        else:
                            Loading.returning("Invalid response. {} attempts remaining. Please try again.".format(2 - j), 2)
                    else:
                        Loading.returning("3 attempts exceeded. Moving on... +0 Reputation.", 3)
                        # Loading.returning("", 2)
                else:
                    Loading.returning(follow_up + (' +' if i.answer else ' -') + str(i.reputation) + ' Reputation.', 3)
                    # Loading.returning(, 2)
                    self.stats.reputation += (i.reputation if i.answer else -i.reputation)
        for i in events:
            if "outing" in i.event:
                match (1, 1, 2, 2, 3, 3)[random.randint(0, 2)]:
                    case 1:
                        # Importance 1, easy to plan, quick event. Same month, within a week, 0.5-1 hours, simple.
                        self.events.append(Event(["Small Hike", "First Aid", "Orienteering", "Knot Training"][random.randint(0, 3)],
                                                 self.time + td(days=random.randint(self.time.day, self.time.day + 7), hours=random.randint(8, 16) - self.time.hour, minutes=[0, 15, 30, 45][random.randint(0, 3)]), 1))
                        Loading.returning(self.events[len(self.events) - 1].alert_message(), 3)
                    case 2:
                        # Importance 2, meh to plan, decent-sized event. Same month, within 2-3 week, 1-3 hours.
                        self.events.append(Event([["Hike", "Rock Climbing", "Coastal Cleanup"] + (["Bowling", "Escape Room"] if not i.answer else [])][random.randint(0, 3)],
                                                 self.time + td(days=random.randint(self.time.day + 7, self.time.day + 21), hours=random.randint(8, 16) - self.time.hour, minutes=[0, 15, 30, 45][random.randint(0, 3)]), 2))
                        Loading.returning(self.events[len(self.events) - 1].alert_message(), 3)
                    case 3:
                        # Importance 3, hard to plan, long event. Within 2 month, 3-8 hours, simple.
                        self.events.append(Event(["Kids Against Hunger", "Conservation Outing"], self.time +
                                                 td(days=random.randint(self.time.day, self.time.day + 30) + random.randint(1, 2) * 30, hours=random.randint(8, 16) - self.time.hour, minutes=[0, 15, 30, 45][random.randint(0, 3)]), 3))
                        Loading.returning(self.events[len(self.events) - 1].alert_message())
                    case 4:
                        self.events.append(Event("Campout", self.time + td(days=random.randint(self.time.day + 7, self.time.day + 28))))

            elif "phone" in i.event and i.answer:
                Loading.returning("Your friend thanks you for giving him advice, and gifts you $5! +$5", 3)
                self.stats.money += 5
            elif "game" in i.event and i.answer:
                if "well" in i.yes_msg:
                    Loading.returning("Your friends awarded you $10 for helping them win the game. +$10", 3)
                    self.stats.money += 10
                elif "awry" in i.yes_msg:
                    Loading.returning("Your friends awarded you $5 for helping out during the game. +$5", 3)
                    self.stats.money += 5
            elif "conference" in i.event and i.answer:
                Loading.returning("Your friend puts in a good word for you with the Scoutmaster.", 3)
        input("The troop meeting has ended." + (" Don't forget to purchase the remaining uniform articles!" if required_uniform else "") + " Press ENTER to head back home.")
        self.events.pop(self.events.index([i for i in self.events if i.name == 'Troop Meeting'][0]))
        self.time = self.time.replace(hour=20, minute=00)
        self.stats.hunger = 40 if self.stats.hunger > 40 else self.stats.hunger
        self.stats.thirst = 40 if self.stats.thirst > 40 else self.stats.thirst
        return

    def phone(self):
        """
        Method for playing on your phone for recreation.
        :return: Nothing
        """
        phone_time = (random.randint(0, 3) + 1) * 15
        if self.stats.hunger <= 0 or self.stats.thirst <= 0:
            Loading.returning("ALERT: Your Health is getting low. Eat or drink something after you use the phone.", 3)
        self.refresh("minute", phone_time)
        print("PHONE: {} Minutes".format(phone_time))
        Loading.returning(["You play on your phone for a bit.", "You have a nice phone session looking at memes.",
                           "You spend 45 whole minutes scrolling on social media.",
                           "Oops! You overspend your phone time and use up an hour."][int(phone_time / 15) - 1], 3)
        return

    def console(self):
        """
        Method for playing on your game console for recreation.
        :return: Nothing
        """
        console_time = (random.randint(0, 3) + 1) * 20
        if self.stats.hunger <= 0 or self.stats.thirst <= 0:
            Loading.returning("ALERT: Your Health is getting low. Eat or drink something after you play games.", 3)
        self.refresh("minute", console_time)
        print("GAME CONSOLE: {} Minutes".format(console_time))
        Loading.returning(["You take a quick break and play some games.", "You play for quite a bit and have some good fun.",
                           "You spend an hour playing with friends and having a great time.",
                           "Oops! You lose track of time and play for a while. It was still fun."
                           "."][int(console_time / 20) - 1], 3)
        return

    def show_rank(self):
        """
        Method to show ranks and requirements.
        :return: Nothing.
        """
        print("Current Rank: " + self.rank.rank.capitalize())
        print("Requirements:\n" + '\n'.join(("COMPLETE" if i.status else "INCOMPLETE") + ':\t' + i.name for i in self.rank.requirement_list))
        if input("Press ENTER to continue.") == 'debug':
            oath = (input("The Scout Oath.\n_______, I will do my best...").lower() == 'on my honor', input("To _____ to God and my country...").lower() == 'do my duty',
                    input("To ______...").lower() == "obey the scout law", input("To help other people ________").lower() == "at all times",
                    input("To keep myself ______, ______, and _______").lower() in ("physically strong mentally awake morally straight", "physically strong, mentally awake, and morally straight",
                                                                                    "physically strong mentally awake and morally straight", "physically strong, mentally awake, morally straight"))
            if all(oath):
                Loading.returning("Great Job!", 2)
            else:
                Loading.returning("Oops! You got some wrong. Try again later.", 2)
            if (input("The Scout law.\nType all the tenets of the Scout law in order, separated by commas, like this: \"Lorem, Ipsum, Dolor, Sit, Amet\"").lower() ==
                    "trustworthy, loyal, helpful, friendly, courteous, kind, obedient, cheerful, thrifty, brave, clean, friendly"):
                Loading.returning("Great Job!", 2)
                [i.status for i in self.rank.requirement_list if "scout oath" in i][0] = True
            else:
                Loading.returning("Oops! You got some wrong. Try again later.", 2)
        return

    def hike(self, size):
        """
        Method for both of the hiking events
        :param size: Size of the outing. String
        :return: Nothing.
        """

        class HikingEvent:
            """
            Class HikingEvent.
            Creates an object to store an event during the hiking outing. Stores similar to MeetingEvent: event name, yes and no messages, and stat changes for yes and no.
            """

            def __init__(self, event, yes_msg='', no_msg='', event_yes='', event_no=''):
                self.event = event
                self.yes_msg = yes_msg
                self.no_msg = no_msg
                self.event_yes = event_yes
                self.event_no = event_no
                return

        Loading.returning("Welcome to the hike!")
        shoes = False
        if [i for i in self.possessions if 'shoes' in i.name]:
            shoes = True
        else:
            if input("The outing leader strongly recommends shoes on this outing. Proceed or stay back?").lower() in ("proceed", "yes", "y", "ok"):
                Loading.returning("You proceed with the hike...", 2)
            else:
                Loading.returning("You decide to stay back on the outing.", 2)
                return
        events = [HikingEvent(i[0], i[1], i[2], i[3], i[4]) for i in [
            ("You spot some three-leaved clover-looking plants that are dripping some sort of sap. Touch it?", "Oh no! You touch it and your finger becomes very itchy. -5 Health",
             "Good job. Three-leaved clover plants are usually poison oak.", "self.stats.health -= 5", "pass"),
            ("You get hungry and want to eat something. Pull a bar out of your pack to eat or no?", "You pull out a bar and eat, but you hold the group up. -5 Reputation.",
             "You continue on the hike but you get more hungry. -10 Hunger", "self.stats.reputation -= 5", "self.stats.hunger -= 10"),
            ("There's a hill coming up. Run up it to get to the front?", "You run up the hill and get to the top, but you're very tired. -5 Hunger, -10 Thirst.", "You stay in the middle and keep your pace.",
             "self.stats.hunger -= 5 ; self.stats.thirst -= 10", "pass"),
            ("You see a down hill section ahead. Run down it and have some fun?", "You run down the hill until you trip on a rock and scrape yourself. -5 Health.",
             "You decide against it and stick with the group. +5 Reputation", "self.stats.health -= 5", "self.stats.reputation += 5"),
            ("The leader asks you if you think the hike is going well. Yes or no?", "The leader is glad you're enjoying yourself.", "The leader is sad you don't like it.", "pass", "pass"),
            ("You're getting thirsty. Pull out your water bottle to drink some water?", "Your leader sees you pull your bottle out and calls for a water break. +10 Thirst.",
             "You keep hiking and get more thirsty. -10 Thirst.", "self.stats.thirst += 10", "self.stats.thirst -= 10")]]
        if shoes:
            events.append(("There is a large muddy spot that looks shallow to you. Jump in it for the fun?", "You happily jump in the mud puddle, however it turns out to be a pool. - 1 pair of Shoes",
                           "You decide against jumping in the puddle and walk around it.", "self.possessions.remove([i for i in self.possessions if 'shoes' in i.name][0])", "pass"))
        for i in random.sample(events, (6 if size == "big" else 3)):x
            for j in range(3):
                if i.event:
                    choice = input(i.event)
                    if "yes" in choice:
                        Loading.returning(i.yes_msg, 2)
                        exec(i.event_yes)
                        break
                    elif "no" in choice:
                        Loading.returning(i.no_msg, 2)
                        exec(i.event_no)
                        break
                    else:
                        Loading.returning("Invalid response. {} attempts remaining. Please try again.".format(2 - j), 2)
                else:
                    break
            else:
                Loading.returning("3 attempts exceeded. Moving on...", 3)
        input("The hike is finished. Well done. Press ENTER to return home.")
        self.refresh("minute", (30 if size == "small" else 90))
        return

    def first_aid(self):
        """
        Method for the First Aid Outing.
        :return: Nothing.
        """

        class FirstAidQuestion:
            """
            Class FirstAidQuestion.
            Creates an object to store a question during this outing. Stores the question, multiple choice options, and the correct answer.
            """

            def __init__(self, question, options, answer):
                self.question = question
                self.options = options
                random.shuffle(self.options)
                self.answer = answer

        Loading.returning("Welcome to the first aid outing.", 2)
        Loading.returning("Here you will be tested on your first aid. Good Luck!", 3)
        score = 0
        for i in random.sample([FirstAidQuestion(i[0], i[1], i[2]) for i in [
                ("What does AED stand for?", [": Automated Emergency Drill", ": Automatic Excess Drainer", ": Automated External Defibrillator", ": Autocratic Extrinsic Deoscillator"], ": Automated External Defibrillator"),
                ("What do you do in the event of a severe allergic reaction?", [": Run around", ": Use an Epi-Pen", ": Inject epinephrine into your system while doing push-ups.", ": Do nothing."], ": Use an Epi-Pen"),
                ("What happens if you break a bone in an outing?", [": Use a tourniquet to reduce movement of the limb.", ": Flee from the scene", ": Amputate the limb.", ": Cry out for help"], ": Use a tourniquet to reduce movement of the limb."),
                ("Put the steps for alleviating a cut or scrape in order.", [": Wash, Sanitize, Cover", ": Sanitize, Cover, Wash", ": Cover, Wash, Sanitize", ": Sanitize, Wash, Cover"], ": Wash, Sanitize, Cover"),
                ("Why do we wear mask during an airborne pandemic?", [": To protect ourselves and others.", ": To protect others", ": To look cool by buying your favorite design.", ": To scare the virus."], ": To protect ourselves and others.")]], 3):
            choice = input('\n' + i.question + '\n' + '\n'.join([["A", "B", "C", "D"][j] + i.options[j] for j in range(len(i.options))]) + '\n')
            if choice in i.answer or choice in ["A", "B", "C", "D"][i.options.index(i.answer)]:
                Loading.returning("Great Job!", 2)
                score += 1
            else:
                Loading.returning("Sorry, that's incorrect. The correct answer was{}".format(i.answer), 5)
        input("The First Aid outing is over. You scored {}/3. +{} Reputation\nPress ENTER to return home.".format(score, score * 5))
        self.refresh("minute", 15)
        return

    def orienteering(self):
        """
        Method for the orienteering outing.
        :return: Nothing.
        """
        Loading.returning("Welcome to Orienteering!", 2)
        print("State the sequence of aligning a compass.")
        sequence = (input("Rotate the dial to _____").lower() == "north", input("Align the _____ with north.").lower() == "needle", input("_____ the dial to the specified degree").lower() == "rotate",
                    input("Align with _____").lower() == "north")
        if all(sequence):
            Loading.returning("Great job!", 2)
        else:
            Loading.returning("Oops! You got some wrong.", 2)
        input("The orienteering outing is over. Well done. Press ENTER to return home.")
        self.refresh("minute", 15)
        return

    def knot_training(self):
        """
        Method to train the player in knots.
        :return: Nothing.
        """

        def valid_move(message, knot_list):
            """
            Method to make sure the user input is a valid move
            :param message: User Input
            :param knot_list: List of knot steps
            :return: Boolean if the move is valid or not
            """
            message = message.split(' ')
            if len(message) == 2:
                return (message[0] in ''.join([str(i) for i in range(1, len(knot_list) + 1)]) and message[1] in ('up', 'down')) and ((message[1] == 'up' and '1' not in message[0]) or (message[1] == 'down' and str(len(knot_list)) not in message[0]))
            else:
                return False

        Loading.returning("Welcome to Knot Training!", 2)
        square_knot = ['right over left', 'tie around', 'left over right', 'tie around']
        shuffle = square_knot.copy()
        while square_knot == shuffle:
            random.shuffle(shuffle)
        print("Move the items up and down to display the correct way to make a square knot.")
        while square_knot != shuffle:
            print('\n'.join(str(i + 1) + '. ' + shuffle[i].capitalize() for i in range(len(shuffle))))
            action = input("What would you like to move? Type the number of the step and either \"up\" or \"down\" (E.g. \"2 up\", \"3 down\"")
            if valid_move(action, shuffle):
                action = action.split(' ')
                action = (int(action[0]) - 1, action[1])
                buffer = shuffle[action[0]]
                shuffle[action[0]] = shuffle[action[0] - 1 if action[1] == 'up' else action[0] + 1]
                shuffle[action[0] - 1 if action[1] == 'up' else action[0] + 1] = buffer
            else:
                Loading.returning("Please type a valid move.", 2)
        Loading.returning("Well done!", 2)
        # UPDATE Add more knots
        input("The knot training outing has ended. Press ENTER to return home.")
        self.refresh("minute", 20)
        return

    def rock_climbing(self):
        """
        Method for the rock climbing outing.
        :return: Nothing.
        """
        Loading.returning("Welcome to the rock climbing outing.", 2)
        if 'yes' in input("Would you like to view the instructions? \"yes\" or \"no\"").lower():
            input("Rock climbing is easy! \nThe X's at the bottom of the screen are your feet.\nThere will rocks in front of you and all you have to do is type \"left\" or \"right\"!\n"
                  "Once you make it to the top, you can ring the bell and then come on down. \n\nPress ENTER to continue.")
        board = [
            """

   __
  |__|    __
         |__|

""", """
   __
  |__|   
          __
         |__|

""", """

          __
   __    |__|
  |__|
  
""", """
          __
         |__|
   __
  |__|
"""]
        height = 1
        frame = random.randint(0, 3)
        while height <= 10:
            print(board[frame])
            print("   X       X   ")
            print("Height: " + str(height))
            action = input("Left or right?").lower()
            if action in ("left", "right"):
                match frame:
                    case 0:
                        if action == "left":
                            height -= (1 if height > 1 else 0)
                            Loading.returning("Oh no! You almost make it, but you slip.", 2)
                        elif action == "right":
                            height += 1
                        frame = random.randint(2, 3) if height > 1 else frame
                    case 1:
                        if action == "left":
                            height -= (1 if height > 1 else 0)
                            Loading.returning("Oh no! You slip and fall down.", 2)
                        elif action == "right":
                            height += 1
                        frame = random.randint(2, 3) if height > 1 else frame
                    case 2:
                        if action == "left":
                            height += 1
                        elif action == "right":
                            height -= (1 if height > 1 else 0)
                            Loading.returning("Oh no! You almost make it, but you slip.", 2)
                        frame = random.randint(0, 1) if height > 1 else frame
                    case 3:
                        if action == "left":
                            height += 1
                        elif action == "right":
                            height -= (1 if height > 1 else 0)
                            Loading.returning("Oh no! You slip and fall down.", 2)
                        frame = random.randint(0, 1) if height > 1 else frame
        Loading.returning("DING DING DING! Hooray! You have climbed to the top.", 2)
        input("The Rock Climbing outing has finished. Well done. Press ENTER to return home.")
        self.refresh("minutes", 90)
        return

    def coastal_cleanup(self):
        """
        Method for the Coastal Cleanup outing.
        :return: Nothing.
        """
        # First, generate a new board.
        Loading.returning("Welcome to the Coastal Cleanup.", 2)
        if 'yes' in input("Would you like to view the instructions? \"yes\" or \"no\"").lower():
            input("The coasts are littered with trash! Your job is to clean the coast of its filthy litter and restore it to a life-fulfilling utopia.\n"
                  "Sand and Rocks are marked with \"S\" and \"R\". Trash is marked with \"T\", \"X\", \"B\", and \"G\".\nCount the pieces of trash, "
                  "and take back your coast!\n\nPress ENTER to continue.")
        score = 0
        for _ in range(5):
            board = [["S" if random.randint(0, 1) == 0 else "R" for _ in range(20)] for _ in range(10)]
            pieces = random.randint(1, 5)
            for (x, y) in [[random.randint(0, 9), random.randint(0, 19)] for _ in range(pieces)]:
                board[x][y] = ["T", "X", "B", "G"][random.randint(0, 3)]
            print('\n'.join(' '.join(y for y in x) for x in board))
            action = input("How many pieces of trash do you see?")
            while True:
                if action in '0123456789':
                    if int(action) == pieces:
                        Loading.returning("Well done!", 2)
                        score += 1
                    else:
                        Loading.returning("Sorry, there were {} pieces of trash.".format(pieces), 2)
                    break
                else:
                    Loading.returning("Please type a valid response.")
        input("The coastal cleanup outing has ended. " + ("Excellent Work! " if score == 10 else "Well done! ") + "Press ENTER to return home.")
        self.refresh("minute", 150)
        return

    def bowling(self):
        """
        Method for the Bowling outing.
        :return: Nothing.
        """
        Loading.returning("Welcome to the Bowling Outing.", 2)
        if 'yes' in input("Would you like to view the instructions? \"yes\" or \"no\""):
            input("It's time to bowl! Type the number of the lane with the pin to score a strike, minding the angle.\nGet the highest score!\n\nPress ENTER to continue.")
        pin = """
{}.o.
{}|_|
"""
        score = 0
        for i in range(5):
            space = random.randint(0, 6)
            angle = random.randint(-3, 3)
            print(pin.format(' ' * space, ' ' * space))
            print(" ^^^^^^^\n 1234567\nAngle: {}".format(angle))
            action = input("Which lane?")
            if action in "0123456789":
                if int(action) == space + 1 + angle:
                    Loading.returning("Great job!", 2)
                    score += 1
                elif int(action) == space + angle or int(action) == space + 2 + angle:
                    Loading.returning("So close!", 2)
                else:
                    Loading.returning("Oh no! Miss!", 2)
        input("The Bowling outing has ended. " + ("Extraordinary Bowling! " if score == 5 else "Well done. ") + "Press ENTER to return home.")
        self.refresh("minute", 120)
        return

    def escape_room(self):
        """
        Method for the Escape Room Outing.
        :return: Nothing.
        """
        Loading.returning("Welcome to the Escape Room.", 2)
        if 'yes' in input("Would you like to view the instructions? \"yes\" or \"no\""):
            input("Escape! Your objective is to solve puzzles to escape the dungeon.\nYou will solve puzzles such as: Color Sequence match, Laser Maze, and Circuit Fix.\n"
                  "For the Color Sequence Match, just type in the colors stated on screen. Copy the pattern to escape.\n"
                  "For the Laser Maze, you must maneuver around the lasers on screen. Your body size is 3, and you must move in and out to escape.\n"
                  "For the Circuit Fix, you must identify which wires connect by typing in the numbers of the terminals to connect them. Fix the board and you're out!\n\n"
                  "Press ENTER to continue.")
        # Color Sequence Match first.
        colors = ["red", "yellow", "green", "blue", "purple", "orange"]
        display = [colors[random.randint(0, 5)]]
        i = 0
        while i < 5:
            for j in display:
                print(j.capitalize() + '\r', end='')
                time.sleep(1)
            print('\r')
            action = input("What was the sequence?\r").lower()
            if action == ' '.join(display):
                Loading.returning("Well done!", 2)
                i += 1
            else:
                Loading.returning("Try again!", 2)
                continue
            display.append(colors[random.randint(0, 5)])
        Loading.returning("Great Job!", 2)

        # Now for the laser maze.
        Loading.returning("Now for the laser maze. Remember not to hit the laser!")

        def get_board():
            """
            Method to generate a new laser board.
            :return: Nothing.
            """
            new_space = random.randint(1, 5)
            new_board = ('\n' * new_space) + '--------------------' + ('\n' * (7 - new_space))
            return new_board, new_space

        score = 0
        i = 0
        while i < 5:
            board, space = get_board()
            print(board)
            action = input("Which direction? \"down\" or \"up\"")
            if action in ('down', 'up'):
                if action == "down" and space <= 3:
                    score += 1
                elif action == "up" and space >= 3:
                    score += 1
                else:
                    Loading.returning("Oh no! You hit a laser.", 2)
                    break
                i += 1
            else:
                Loading.returning("Type a valid answer.", 2)
        Loading.returning("Great Job!" if score == 5 else "Good effort." if score > 0 else "Moving on...", 2)

        # Now for the circuit fix.
        def valid_move(user_input):
            """
            Method to make sure the user input is a valid move
            :param user_input: User input to check
            :return: Boolean if the move is valid or not.
            """
            user_input = user_input.split(' ')
            if len(user_input) == 3:
                return all([element[0] in '123' and element[1] in 'abc' for element in user_input])
            else:
                return False

        # UPDATE Add more circuits
        circuits = ["""
1 o--,    ,-,    ,--o a
     '--, | '--, |     
2 o-----|-' ,--|-',-o b
        '---|-,'--'    
3 o---------' '-----o c
""", """
1 o-, ,-----,    ,--o a
    | |     | ,--'     
2 o-|-',----|-'   ,-o b
    '--|----|-----'    
3 o----'    '-------o c
""", """
1 o-, ,----,    ,---o a
    '-|--, | ,--|-,     
2 o---',-|-|-',-' '-o b
       | '-|--',--,    
3 o----'   '---'  '-o c
"""]
        selection = random.randint(0, 2)
        while True:
            print(circuits[selection])
            action = input("Type the connections out in numerical order. E.g. \"1a 2b 3c\".")
            if valid_move(action):
                if action == ['1c 2b 3a', '1b 2c 3a', '1a 2c 3b'][selection]:
                    break
                else:
                    Loading.returning("Sorry, that's incorrect.", 2)
                    continue
            else:
                Loading.returning("Type a valid answer.", 2)
        Loading.returning("Excellent Work! You escaped.", 2)
        input("The Escape Room outing has ended. Press ENTER to return home.")
        self.refresh("minute", 180)
        return

    @DeprecationWarning
    def cert_outing(self):
        """
        Method for the CERT Outing.
        Brainstorming: What happened on the CERT Outing? Uhhhh Let's see... We put on make-up, go into the fake building, and wait for the starting bell to ring. Then we wait
        for the "officials" to walk in, and then we shout and scream in agony. This whole thing isn't exactly for us, it's for the "officials". Maybe I'll scrap this one...
        :return: Nothing.
        """
        Loading.returning("Welcome to the CERT Outing.", 2)
        if 'yes' in input("Would you like to view the instructions? \"yes\" or \"no\""):
            input("")

    def kids_against_hunger(self):
        """
        Method for the Kids Against Hunger Outing.
        :return: Nothing.
        """
        class Meal:
            """
            Class Meal.
            Creates an object to store a Meal. Stores the name and creates and stores the count and the progress towards the next meal.
            """
            def __init__(self, name):
                self.name = name
                self.count = 0
                match self.name:
                    case 'breakfast':
                        self.current = {"grain": False, "orange": False, "powdered milk": False}
                    case 'lunch':
                        self.current = {"bread": False, "peanut butter": False, "jelly": False}
                    case 'dinner':
                        self.current = {"rice": False, "carrot": False, "peach": False}

            def add(self, name, add_back):
                """
                Method to change the status of present foods in the meal object
                :param name: Name of the meal
                :param add_back: If the meal is complete, add the foods back to the pool
                :return: Nothing.
                """
                self.current[name] = True
                if all([self.current[food] for food in self.current]):
                    self.count += 1
                    self.current.update((i, False) for i in self.current)
                    Loading.returning("Well done!", 1)
                    add_back.extend([i for i in self.current])

            def __repr__(self):
                return ("{} - Meals: {}" + ('\t' if self.name == "breakfast" else '\t\t') + "{} ").format(self.name.capitalize(), ('|' * self.count if self.count > 0 else "0"), ','.join([i.capitalize() for i in self.current if self.current[i]]))

        Loading.returning("Welcome to Kids Against Hunger.", 2)
        if 'yes' in input("Would you like to view the instructions? \"yes\" or \"no\""):
            input("Here at KAH, we package food to be eaten by kids all across the world, mainly those without access to a stable food supply.\n"
                  "Today during your visit, you'll also be packaging food. Select the correct meal for the shown foods.\n"
                  "A Breakfast needs some GRANOLA, a ORANGE, and a pack of POWDERED MILK.\n"
                  "A Lunch needs BREAD, a packet of PEANUT BUTTER, and a packet of JELLY.\n"
                  "A Dinner needs a box of RICE, a full CARROT, and a PEACH.\n\n"
                  "Good Luck! Press ENTER to continue.")
        foods = ["grain", "orange", "powdered milk", "bread", "peanut butter", "jelly", "rice", "carrot", "peach"]
        meals = [Meal(i) for i in ('breakfast', 'lunch', 'dinner')]
        population = foods.copy()
        random_food = population[random.randint(0, len(population) - 1)]
        i = 0
        while i < 25:
            print('\n' + '\n'.join([j.__repr__() for j in meals]))
            action = input("Where does {} go?".format(random_food))
            if action in ('breakfast', 'lunch', 'dinner'):
                action = [j for j in meals if j.name == action][0]
                if random_food in action.current:
                    population.remove(random_food)
                    action.add(random_food, population)
                    if not population:
                        population = foods.copy()
                    random_food = population[random.randint(0, len(population) - 1)]
                    i += 1
                else:
                    Loading.returning("That's the wrong meal pack.", 2)
            else:
                Loading.returning("Enter a meal name.", 2)
        Loading.returning("Well done! Your grand total was {} breakfast{}, {} lunch{}, and {} dinner{}.".format(
            meals[0].count, 's' if meals[0].count != 1 else '', meals[1].count, 's' if meals[1].count != 1 else '', meals[2].count, 's' if meals[2].count != 1 else ''))
        input("The KAH Outing has ended. Press ENTER to return home.")
        self.refresh("hour", 5)
        return

    def conservation_outing(self):
        """
        Method for the Conservation Outing.
        :return: Nothing.
        """
        class Bin:
            """
            Class Bin.
            Creates an object to store a Bin. Stores the name and count of how many things are in it.
            """
            def __init__(self, name):
                self.name = name
                self.count = 0

            def __repr__(self):
                return "{} - \t{} ".format(self.name.capitalize(), ('|' * self.count if self.count > 0 else "0"))
        Loading.returning("Welcome to the conservation outing.")
        if 'yes' in input("Would you like to view the instructions? \"yes\" or \"no\""):
            input("Reduce, Reuse, Recycle! Here we're going to learn where to place what item of waste. Specifically which bin (trash, recycle, compost).\n"
                  "We need to preserve our environment and the first way we can do that is to limit our contribution to the city landfill. Recycling and composting is the way to go!\n"
                  "Make your best guess as to what goes in the trash, recycle, and compost, and type it in. The item will be sorted.")
        bins = [Bin(i) for i in ('garbage', 'recycle', 'compost')]
        garbage = ["battery", "broken plate", "diaper"]
        recycle = ["paper plate", "used phonebook", "old envelopes"]
        compost = ["broken egg", "apple core", "dead leaf"]
        random_item = (garbage + recycle + compost)[random.randint(0, len(garbage + recycle + compost) - 1)]
        i = 0
        while i < 20:
            print('\n' + '\n'.join([j.__repr__() for j in bins]))
            action = input("Where does {} go?".format(random_item))
            if action in [j.name for j in bins]:
                if (random_item in garbage and action == 'garbage') or (random_item in recycle and action == 'recycle') or (random_item in compost and action == 'compost'):
                    [j for j in bins if j.name == action][0].count += 1
                    Loading.returning("Great work!", 1)
                    random_item = (garbage + recycle + compost)[random.randint(0, len(garbage + recycle + compost) - 1)]
                    i += 1
                else:
                    Loading.returning("That's the wrong pile.", 2)
            else:
                Loading.returning("Type a valid pile.", 2)
        input("The Conservation outing is finished. Well done. Press ENTER to return home.")
        self.refresh("hour", 5)

    def defeat(self):
        """
        Method for 0 Health! Oh no!
        :return: Nothing.
        """
        Loading.returning("Oh no!", 2)
        Loading.returning("Your health is very low.", 2)
        if self.stats.hunger == 0.0:
            Loading.returning("You are extremely hungry.", 2)
            if self.stats.thirst == 0.0:
                Loading.returning("You are also extremely dehydrated.", 2)
        elif self.stats.thirst == 0.0:
            Loading.returning("You are extremely dehydrated.", 2)
        Loading.returning("In order to remedy the problem, you are rushed to the emergency room.", 3)
        Loading.returning("Fortunately, they were successful.", 2)
        Loading.returning("However, your condition will never permit you to pursue Scouts ever again.", 3)
        Loading.returning("DEFEAT: Your scouting journey was ended prematurely and you will never reach your ultimate goal of the Eagle Rank.", 5)
        input("Press ENTER to delete your game file.")
        if not self.new_file:
            os.remove(self.path + '\\' + self.filename)
        if 'yes' in input("Would you like to try again?"):
            return 1
        else:
            Loading.returning_to_apps()
            return 0
