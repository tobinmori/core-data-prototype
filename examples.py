from models import Series, Franchise, SubSeries, Season, \
    Image, Station, Producer, Distributor, Audience, SeriesEpisode, OneTimeOnlyEpisode, SeasonAssociation, SeriesRelationTag
from session_manager import session

def test1():
    """Franchised, Series, 1 Season, 1 Ep"""
    p = Producer(name='BBC Productions')
    p.save()

    d = Distributor(name='PBS Distribution')
    d.save()

    ep1 = SeriesEpisode(name="Wolf Hall Ep 1")
    ep1.save()

    se = Season(name="1", ordinal="1")
    se.save()

    s = Series(name='Wolf Hall')
    s.orgs = [p, d]
    s.save()

    sa = SeasonAssociation(season=se)
    sa.series = s
    sa.episode = ep1
    sa.season = se
    sa.save()

    f = Franchise(name='Masterpiece')
    f.serieses.append(s)
    f.save()

def test2():
    """Franchised, Series, NO Season, 1 OTO"""
    p = Producer(name='BBC Productions')
    p.save()

    d = Distributor(name='PBS Distribution')
    d.save()

    ep1 = OneTimeOnlyEpisode(name="Downton Abbey 2014 X-mas Special")
    ep1.save()

    s = Series(name='Downton Abbey')
    s.onetimeonlys = [ep1]
    s.orgs = [p, d]
    s.save()

    # get the previous
    f = session.query(Franchise).filter(Franchise.name=="Masterpiece").all()[0]
    f.serieses.append(s)
    f.save()

def test3():
    """Franchised, Series, Seasoned, with 1 OTO"""
    p = Producer(name='BBC Productions')
    p.save()

    d = Distributor(name='PBS Distribution')
    d.save()

    ep1 = SeriesEpisode(name="Scandal in Belgravia")
    ep1.save()

    se = Season(name="Season 2", ordinal="2")
    se.save()

    s = Series(name='Sherlock')
    s.orgs = [p, d]
    s.save()

    sa = SeasonAssociation(season=se)
    sa.series = s
    sa.episode = ep1
    sa.season = se
    sa.save()

    # get the previous
    f = session.query(Franchise).filter(Franchise.name=="Masterpiece").all()[0]
    f.serieses.append(s)
    f.save()

def test4():
    """Franchised series with 1 oto"""
    p = Producer(name='Ken Burns')
    p.save()

    d = Distributor(name='PBS Distribution')
    d.save()

    ep1 = SeriesEpisode(name="The Scripture of Nature (1851-1890)")
    ep1.save()

    se = Season(name='Season 2009', ordinal=2009)
    se.save()

    s = Series(name='The National Parks')
    s.orgs = [p, d]
    s.save()

    sa = SeasonAssociation(season=se)
    sa.series = s
    sa.episode = ep1
    sa.season = se
    sa.save()

    f = Franchise(name='Ken Burns')
    f.serieses = [s]
    f.save()

def test5():
    """Series with Ep in one season AND Subseries with Ep in a different season"""
    p = Producer(name='WGBH Productions')
    p.save()

    d = Distributor(name='PBS Distribution')
    d.save()

    se = Season(name='38', ordinal=38)
    se.save()

    se1 = Season(name='1', ordinal=1)
    se1.save()

    e1 = SeriesEpisode(name="Making Stuff Similar Episode")
    e1.save()

    e2 = SeriesEpisode(name="Making Stuff Similar Episode2")
    e2.save()

    ss1 = SubSeries(name="Making Stuff")
    ss1.save()

    s = Series(name="NOVA")
    s.subseries = [ss1]
    s.save()

    sa = SeasonAssociation(season=se)
    sa.series = s
    sa.episode = e1
    sa.save()

    sa2 = SeasonAssociation(season=se1)
    sa2.series = ss1
    sa2.episode = e2
    sa2.save()

def test6():
    """Series with OTO"""
    p = Producer(name='WGBH Productions')
    p.save()

    d = Distributor(name='PBS Distribution')
    d.save()

    se = Season(name='38', ordinal=38)
    se.save()

    e1 = OneTimeOnlyEpisode(name="Surviving Ebola")
    e1.seasons = [se,]
    e1.save()

    # get the previous
    s = session.query(Series).filter(Series.name=="NOVA").all()[0]
    s.seasons = [se,]
    s.episodes = [e1,]
    s.save()

    sa = SeasonAssociation(season=se)
    sa.series = s
    sa.episode = e1
    sa.save()

def test7():
    """Series with Subseries and 1 Ep"""
    p = Producer(name='WGBH Productions')
    p.save()

    d = Distributor(name='PBS Distribution')
    d.save()

    se = Season(name='17', ordinal=17)
    se.save()

    e1 = SeriesEpisode(name="Antiques Roadshow Seattle, Ep1")
    e1.seasons = [se,]
    e1.save()

    sss = Season(name='1', ordinal=1)
    sss.save()

    ss1 = SubSeries(name="Antiques Roadshow in Seattle")
    ss1.save()

    s = Series(name="Antiques Roadshow")
    s.subseries = [ss1]
    s.seasons = [se,]
    s.save()

    sa = SeasonAssociation(season=se)
    sa.series = s
    sa.episode = e1
    sa.save()

    sa2 = SeasonAssociation(season=sss)
    sa2.series = ss1
    sa2.episode = e1
    sa2.save()

def test8():
    """Series with EP"""

    p = Producer(name='WETA')
    p.save()

    d = Distributor(name='PBS Distribution')
    d.save()

    ep1 = SeriesEpisode(name="Monday, July 15th, 2014")
    ep1.save()

    s = Series(name='PBS NewsHour')
    s.orgs = [p, d]
    s.save()

    se = Season(name='29', ordinal=29)
    se.save()

    sa2 = SeasonAssociation(season=se)
    sa2.series = s
    sa2.episode = ep1
    sa2.save()

def test9():
    """WEIRD ONE: Series and Subseries of different seasons sharing the same Ep"""
    p = Producer(name='WETA Productions')
    p.save()

    d = Distributor(name='PBS Distribution')
    d.save()

    se = Season(name='41', ordinal=41)
    se.save()

    se2 = Season(name='2012', ordinal=2012)
    se2.save()

    e1 = SeriesEpisode(name="Democratic National Convention September 5, 2015 Part 1")
    e1.save()

    ss1 = SubSeries(name="Elections")
    #ss1.episodes = [e1,]
    ss1.seasons = [se2]
    ss1.save()

    s = session.query(Series).filter(Series.name=="PBS NewsHour").all()[0]
    #s = Series(name="PBS NewsHour")
    s.subseries = [ss1]
    s.seasons = [se,]
    s.save()

    sa = SeasonAssociation(season=se)
    sa.series = s
    sa.episode = e1
    sa.save()

    sa2 = SeasonAssociation(season=se2)
    sa2.series = ss1
    sa2.episode = e1
    sa2.save()

def test10():
    """Series with OTO"""
    p = Producer(name='CAPC')
    p.save()

    d = Distributor(name='PBS Distribution')
    d.save()

    e1 = OneTimeOnlyEpisode(name="A Capitol Fourth 2014")
    e1.save()

    s = Series(name="A Capitol Fourth")
    s.onetimeonlys = [e1,]
    s.save()

def test1112():
    """Series with 1 ep (in a season) and 1 OTO (seasonless)"""
    p = Producer(name='Universal')
    p.save()

    d = Distributor(name='PBS Distribution')
    d.save()

    se = Season(name='3', ordinal=3)
    se.save()

    e1 = SeriesEpisode(name="Go West Young Monkey")
    e1.seasons = [se,]
    e1.save()

    e2 = OneTimeOnlyEpisode(name="Curious George XMAS")
    e2.save()

    s = Series(name="Curious George")
    s.onetimeonlys = [e2,]
    s.save()

    sa = SeasonAssociation(season=se)
    sa.series = s
    sa.episode = e1
    sa.save()

def unfurl(show):
    # Show Series
    print "    "
    print '*Type: ', show.type
    print 'Name: ', show.name
    ## EXPERIMENTAL TAG SYSTEM
    print 'Tag Relation: ', [(t.parent.name, t.child.name, t.tag) for t in show.tags]
    print 'Children (via Tags): ', show.children, [s.name for s in show.children]
    print 'Parents (via Tags): ', show.parents, [s.name for s in show.parents]

    if hasattr(show, 'orgs'):
        print '  - Orgs: ', [(s.name, s.type) for s in show.orgs]
    if hasattr(show, 'franchise') and show.franchise:
        print '  - Franchise:', show.franchise.name
    if hasattr(show, 'images'):
        print '  - Images:', [s.name for s in show.images]

    # Iterate through Seasons to find Eps
    if hasattr(show, 'season_associations') and len(show.season_associations) > 0:
        for season in show.season_associations:
            print "    *Type:", season.episode.type
            print "    Name:", season.episode.name
            print "      - Season:", season.season.ordinal
            if hasattr(season.episode, 'orgs'):
                print '      - Orgs: ', [(s.name, s.type) for s in season.episode.orgs]
            if hasattr(season.episode, 'images'):
                print '      - Images: ', [s.name for s in season.episode.images]
    # If NO Seasons, we presume it's OTO
    if hasattr(show, 'onetimeonlys') and len(show.onetimeonlys) > 0:
        for ep in show.onetimeonlys:
            print "    *Episode:", ep.name
            print "    Episode Type:", ep.type
            print '      *Orgs: ', [(s.name, s.type) for s in ep.orgs]
            print '      *Images: ', [s.name for s in ep.images]

    if hasattr(show,'subseries'):
        for subseries in show.subseries:
            print '    *Type: ', subseries.type
            print '    Name: ', subseries.name
            print '      - Parent: ', subseries.parents[0].name
            if hasattr(show, 'seasons'):
                print '      - Season:', [s.ordinal for s in subseries.seasons]
            if hasattr(show, 'orgs'):
                print '      - Orgs: ', [(s.name, s.type) for s in subseries.orgs]
            for season in subseries.season_associations:
                print '        *Type: ', season.episode.type
                print '        Name: ', season.episode.name
                print '          - Season: ', season.season.ordinal
        print

def test_get():
    titles = [ "Wolf Hall", "Wolf Hall Subseries", "Downton Abbey", "Sherlock", "The National Parks",
              "NOVA", "Antiques Roadshow", "PBS NewsHour", "A Capitol Fourth", "Curious George"]

    for series in titles:
        s = session.query(Series).filter(Series.name==series).all()
        if s:
            unfurl(s[0])

def test_tag():
    p = Producer(name='BBC Productions')
    p.save()

    d = Distributor(name='PBS Distribution')
    d.save()

    ep1 = SeriesEpisode(name="Wolf Hall Ep 1")
    ep1.save()

    se = Season(name="1", ordinal="1")
    se.save()

    s = Series(name='Wolf Hall')
    s.orgs = [p, d]
    s.save()

    s2 = Series(name='Wolf Hall Subseries')
    s2.orgs = [p, d]
    s2.save()

    #sept = SeriesEpisodeTag(series=s, episode=s2, tag='subseries')
    #sept.save()

    sept = SeriesRelationTag(parent=s, child=s2, tag='subseries')
    sept.save()

    sa = SeasonAssociation(season=se)
    sa.series = s
    sa.episode = ep1
    sa.season = se
    sa.save()

def load_data():
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()
    test8()
    test9()
    test10()
    test1112()

# load_data()
#test_tag()
test_get()


