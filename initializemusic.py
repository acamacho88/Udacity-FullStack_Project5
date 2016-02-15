from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Artist, Base, Album, User

engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# Create the staging zone for all database changes
session = DBSession()


# Create dummy user
User1 = User(name="Filburt Turtle", email="filburtttl@gmail.com",
             picture='https://i.ytimg.com/vi/gt5cl0jmrwA/hqdefault.jpg')
session.add(User1)
session.commit()

# Add the Beatles
beatles = Artist(user_id=1, name="The Beatles")

session.add(beatles)
session.commit()

rubbersoul = Album(user_id=1, name="Rubber Soul", description="Their first undeniable classic, the group shows an affinity for Bob Dylan with thoughtful lyricism",
                     year='1965', numtracks="14", cover='http://www.beatlesinterviews.org/al6.jpg',artist=beatles)

session.add(rubbersoul)
session.commit()


revolver = Album(user_id=1, name="Revolver", description="Heralding the psychedlic era, many believe this is the group's crowning achievment.",
                     year='1966', numtracks="14", cover='http://www.mtv.com/news/photos/b/beck_albums_10232006/Beatles_Revolver.jpg',artist=beatles)

session.add(revolver)
session.commit()

sgtpepper = Album(user_id=1, name="Sgt. Pepper's Lonely Hearts Club Band", description="Possibly the first true concept album, the Beatles combined all of their talents into this massively influential record",
                     year="1967", numtracks="13", cover='http://www.nauert.com/pictures/ransgt.jpg',artist=beatles)

session.add(sgtpepper)
session.commit()

abbeyroad = Album(user_id=1, name="Abbey Road", description="The last album the group recorded is a fitting end to the group's career.",
                     year="1969", numtracks="17", cover='http://cdn.riffraf.net/wp-content/uploads/2013/08/abbey_road.jpg',artist=beatles)

session.add(abbeyroad)
session.commit()


# Add Led Zeppelin
zeppelin = Artist(user_id=1, name="Led Zeppelin")

session.add(zeppelin)
session.commit()


zeppelin1 = Album(user_id=1, name="Led Zeppelin", description="The group's pummeling debut showcased the group's new version of hard rock.",
                     year="1969", numtracks="9", cover='http://assets.rollingstone.com/assets/images/album_review/led-zeppelin-1400176280.jpg',artist=zeppelin)

session.add(zeppelin1)
session.commit()

zeppelin2 = Album(user_id=1, name="Led Zeppelin 2",description="On their second album, Led Zeppelin dashed fears of a sophomore slump with a record containing nothing but classics",
                     year="1969", numtracks="9", cover='http://www.relix.com/images/uploads/about/Relix_Led_Zeppelin_II.jpg',artist=zeppelin)

session.add(zeppelin2)
session.commit()

zeppelin4 = Album(user_id=1, name="Led Zeppelin 4", description="One of the most monolithic albums of all time, Led Zeppelin's fourth remains a landmark in hard rock and heavy metal history",
                     year="1971", numtracks="8", cover='http://ecx.images-amazon.com/images/I/61qTE9kINgL._SX355_.jpg', artist=zeppelin)

session.add(zeppelin4)
session.commit()

physgraffiti = Album(user_id=1, name="Physical Graffiti", description="The band's last undisputed masterpiece, they reached the heights of self-indulgence while still remaining musical and captivating",
                     year="1975", numtracks="15", cover='http://ecx.images-amazon.com/images/I/81EYpEraTVL._SY355_.jpg', artist=zeppelin)

session.add(physgraffiti)
session.commit()

# Add Sex Pistols
sexpistols = Artist(user_id=1, name="Sex Pistols")

session.add(sexpistols)
session.commit()


nmbollocks = Album(user_id=1, name="Never Mind the Bollocks, Here's the Sex Pistols", description="An album that reset the rock landscape and remains possibly the single most influential rock record of all time.",
                     year="1977", numtracks="12", cover='http://www.dejkamusic.com/images/album/large/sex_pistols/never_mind_the_bollocks.jpg', artist=sexpistols)

session.add(nmbollocks)
session.commit()

# Add Metallica
metallica = Artist(user_id=1, name="Metallica")

session.add(metallica)
session.commit()


killemall = Album(user_id=1, name="Kill 'Em All", description="Metallica introduces thrash metal to the masses on their debut album, combining traditional metal and hardcore punk.",
                     year="1983", numtracks="10", cover='http://www.billboard.com/files/metallica-kill-em-all-410cover.jpg', artist=metallica)

session.add(killemall)
session.commit()

ridelightning = Album(user_id=1, name="Ride the Lightning", description="This album dealt with more serious subject matter than their debut, such as nuclear war and suicide.",
                     year="1984", numtracks="8", cover='http://ecx.images-amazon.com/images/I/81OiNtyJ2lL._SY355_.jpg', artist=metallica)

session.add(ridelightning)
session.commit()

masterpuppets = Album(user_id=1, name="Master of Puppets", description="What many consider the greatest metal album, Metallica refined their sound and incorporated intricate complex song structures.",
                      year="1986", numtracks="8", cover='http://cps-static.rovicorp.com/3/JPG_400/MI0001/781/MI0001781614.jpg?partner=allrovi.com', artist=metallica)

session.add(masterpuppets)
session.commit()

blackalbum = Album(user_id=1, name="Metallica", description="Metallica embraced much more convential songwriting, bringing accusations of selling out.  The album was a massive commerical success.",
                     year="1991", numtracks="12", cover='http://www.bilborecords.be/sites/default/files/styles/large/public/Metallica%20-%20Black%20Album.jpg?itok=EjKZ3j3L', artist=metallica)

session.add(blackalbum)
session.commit()

# Add Nirvana
nirvana = Artist(user_id=1, name="Nirvana")

session.add(nirvana)
session.commit()


nevermind = Album(user_id=1, name="Nevermind", description="This album changed everything when it was released, banishing hair metal from the airwaves and paving the way for alternative rock's dominance.",
                     year="1991", numtracks="12", cover='https://timeentertainment.files.wordpress.com/2012/04/ent_nirvana_0418.jpg?w=350&h=350&crop=1', artist=nirvana)

session.add(nevermind)
session.commit()

inutero = Album(user_id=1, name="In Utero", description="The band wanted to produce an album that more accurately produced the sound they had aimed for, at the risk of alienating fans of Nevermind",
                     year="1993", numtracks="12", cover='http://www.billboard.com/files/nirvana-in-utero-album-cover-410.jpg', artist=nirvana)

session.add(inutero)
session.commit()

unpluggedny = Album(user_id=1, name="MTV Unplugged in New York", description="This album was released after Kurt Cobain's suicide and bolstered the artist's reputation as a multitalented musician.",
                     year="1994", numtracks="14", cover='http://www.amiright.com/album-covers/images/album-Nirvana-MTV-Unplugged-in-New-York.jpg', artist=nirvana)

session.add(unpluggedny)
session.commit()


# Add Radiohead
radiohead = Artist(user_id=1, name="Radiohead")

session.add(radiohead)
session.commit()


bends = Album(user_id=1, name="The Bends", description="This was Radiohead emerging from the shadow of the single Creep, trying to prove they were more than a one-trick pony.",
                     year="1995", numtracks="12", cover='http://cdn.albumoftheyear.org/album/the-bends.jpg', artist=radiohead)

session.add(bends)
session.commit()

okcomputer = Album(user_id=1, name="OK Computer", description="Radiohead's followup to The Bends was a brilliantly produced concept album that summed up the unease many felt in the modern world.",
                     year="1997", numtracks="12", cover='http://cps-static.rovicorp.com/3/JPG_400/MI0000/139/MI0000139980.jpg?partner=allrovi.com', artist=radiohead)

session.add(okcomputer)
session.commit()

kida = Album(user_id=1, name="Kid A", description="Again defying expectations, Radiohead made a left turn after OK Computer, incorporating electronic music.",
                     year="2000", numtracks="10", cover='http://cps-static.rovicorp.com/3/JPG_400/MI0000/283/MI0000283510.jpg?partner=allrovi.com', artist=radiohead)

session.add(kida)
session.commit()

inrainbows = Album(user_id=1, name="In Rainbows", description="Radiohead left out their usual social/political commentary and created an album more about personal issues.",
                     year="2007", numtracks="10", cover='http://cdn.albumoftheyear.org/album/in-rainbows.jpg', artist=radiohead)

session.add(inrainbows)
session.commit()


# Add Arctic Monkeys
arcticmonkeys = Artist(user_id=1, name="Arctic Monkeys")

session.add(arcticmonkeys)
session.commit()

whateverpeople = Album(user_id=1, name="Whatever People Say I Am, That's What I'm Not",description="The Arctic Monkeys developed a strong following online and once their debut was released became a huge commercial and critical force.",
                          year="2006", numtracks="13", cover='http://images5.fanpop.com/image/photos/30400000/Whatever-People-Say-I-Am-That-s-What-I-m-Not-Cover-arctic-monkeys-30406402-350-350.jpg', artist=arcticmonkeys)

session.add(whateverpeople)
session.commit()


favouritewn = Album(user_id=1, name="Favourite Worst Nightmare", description="On their second album, the band produced an energetic followup with two large singles",
                     year="2007", numtracks="12", cover='http://ecx.images-amazon.com/images/I/51DizmJh1QL._SY355_.jpg', artist=arcticmonkeys)

session.add(favouritewn)
session.commit()

am = Album(user_id=1, name="AM", description="AM proved to be the band's breakthrough in America, with Do I Wanna Know receiving massive radioplay",
                     year="2013", numtracks="12", cover='http://cps-static.rovicorp.com/3/JPG_400/MI0003/626/MI0003626958.jpg?partner=allrovi.com', artist=arcticmonkeys)

session.add(am)
session.commit()


print "added albums!"
