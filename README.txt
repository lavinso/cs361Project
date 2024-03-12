DESCRIPTION:
This is a fictional dog day care website developed for OSU CS361 Software Engineering I. The website was developed using
Agile Scrum framework and relies on a vaccine verification micro service provided by a classmate. The website
calls the microservice when a user logs into or loads their home page. The microservice evaluates the user's registered
dogs and sends a message back to the website stating whether or not the dogs will need a vaccination in the next 30
days, or are overdue. The website server reads that message and displays a corresponding alert for the user to see.

FUTURE WORK:
Implement a password reset feature
Connect contact us to an email
allow user to view and edit their profile, add billing, address, etc to profile
Add photos to dog profile, allow user to edit
allow two users for one dog (user1 and user2 foreign keys in dog table where user2 can be null)
currently no values are not null in the database. Also altered is string instead of boolean.
could make breeds a select, listing all dog breeds from a table that lists all dog breeds and their size,
then breed would be inserted into the dog table as a foreign key. This would allow easier searching as users can
mistype.


CITATIONS:
style adapted from https://www.blog.duomly.com/how-to-crate-simple-web-page-using-bootstrap-5/
login adapted from: https://github.com/techwithtim/Flask-Web-App-Tutorial/blob/main/website/models.py
contact us adapted from: "Bootstrap Contact Form" Bootstrap 4.1.1 Snippet by kshiti06
https://bootsnipp.com/snippets/qr1zR

Image Citations:
monitoring.png: Excited dog daycare workers playing with small dogs
By AntonioDiaz at adobe stock

dogGroup: Portraying dogs of different breeds being playfully washed and dried in a daycare spa setting, emphasizing
cleanliness and socialization. Generative ...  See More
By bluebeat76 at adobe stock

convenientDog: Bring dog to work day - west highland white terrier on desk with computer
By corners74 at adobe stock

safetyPugs: many dogs playing in a dog day care centrum together outside free
By Bernadett at adobe stock

pug: <a href="https://www.freepik.com/free-photo/pug-dog-isolated-white-background_7012187.htm#query=dog&position=3&
from_view=search&track=sph&uuid=fa72e9e6-ed3f-4da8-934a-68151b3d61bb">Image by timolina</a> on Freepik

logo: <a href="https://www.vecteezy.com/free-vector/dog-logo">Dog Logo Vectors by Vecteezy</a>

reviewer1: Little dog with owner spend a day at the park playing and having fun
By elnariz from adobe stock

reviewer2: Bull-terrier and his owner
By Minerva Studio from adobe stock

reviewer3: Pretty paw-some, isnt he. Portrait of a young woman relaxing with her dog at home.
By Chanelle Malambo/peopleimages.com from adobe stock

grooming: Funny portrait of a welsh corgi pembroke dog showering with shampoo. Dog taking a bubble bath in grooming
salon.
By Masarik from adobe stock

daycare: Pet Boarding
By jb325 from adobe stock

sleeping: Beagle puppy sweet sleeping in dog bed
By GarkushaArt from adobe stock

walking: Dog waiting for walk
By Chalabala from adobe stock

map: <a href="https://www.vecteezy.com/free-vector/camping-map">Camping Map Vectors by Vecteezy</a>

cuteDog: Image by <a href=“https://www.freepik.com/free-photo/purebred-dog-being-cute-studio_15615945.htm#query=dog&
position=0&from_view=search&track=sph&uuid=a0b6c437-f122-4ce0-96a2-a2eea2b09df6">Freepik</a>

indoorPlayground: https://www.cascadekennels.com/finleys-tips-on-finding-a-great-doggie-daycare/

outdoor: https://en.wikipedia.org/wiki/Dog_daycare

happyDog: A happy brown and white Pit Bull Terrier mixed breed dog with a huge smile
By Mary Swift from adobe stock

curiousDog: Portrait of an adorbale mixed breed puppy
By kisscsanad from adobe stock

rollingDog: selective focus of golden retriever dog playing with rubber ball on green lawn
By LIGHTFIELD STUDIOS from adobe stock

playingDog: Two Adult Black-and-tan German Shepherds Running on Ground from pexels.com

sleepingDog: Closeup Photography of Adult Short-coated Tan and White Dog Sleeping on Gray Textile at Daytime from
pexels.com

peakingDog: White Short Coated Dog from pexels.com

dogShower: Bathroom to a dog chow chow By 135pixels from adobe stock

haircut: grooming dogs Spitz Pomeranian in the cabin
By sergo321 from adobe stock

brush: a groomer cuts the hair of a poodle dog with a trimmer
By Irina from adobe stock

THIS WEBSITE USES: flask, flask-SQLAlchemy, flask-Blueprint, flask-login, bootstrap
with Special thanks to Amanda Dohring for providing a vaccine verification microservice that ensures users are
aware if their dog's vaccines will be due in the next 30 days or are overdue.
