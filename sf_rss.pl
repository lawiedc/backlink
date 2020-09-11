#!/usr/bin/perl

use strict;
use DBI;
use XML::RSS;
use lib ".";

# Import the connection info from the auth file
require "myauth.pl";
our ( $DSN, $DB_AUTH );

my ( $title, $link, @res, $count );

my $rss = XML::RSS->new( version => '0.9' );

my $stmt = "select author_first_name, author_surname, author_post_name, link, title, activity from hoo_sf_data order by publication_date desc";

# connect to the database
##DCL - should set commit off
my $dbh = DBI->connect($DSN, (split ':', $DB_AUTH),
                    { RaiseError => 1 }
                      ) ||
         print  "<EM>Couldn't connect $DBI::errstr</EM>\n";

$dbh->do("SET OPTION SQL_BIG_TABLES = 1");

# prepare and execute the statement
my $sth = $dbh->prepare( $stmt );
if ( $DBI::err ) {
    return;
}

$sth->execute();
if ( $DBI::err ) {
    return;
}

$rss->channel(
		title => "Duncan Lawie's SF non-fiction",  
		link => "http://www.hoopoes.com/sf/az.shtml",
		description => "A listing of Duncan's SF reviews, interviews and articles");

$count = 0;
while ( @res = $sth->fetchrow ) {
    if ( $DBI::err ) {
        return;
    }

    $title = "$res[4] - $res[0] $res[1] $res[2] ( $res[5] )";
    $link = $res[3];

    $rss->add_item( title => $title, link => $link );

    $count++;

    last if ( $count >= 10 );

}

open RSS, ">/home/hoopoes/www/hoopoes.com/sf/dcl_sf.rss";
print RSS $rss->as_string;
close RSS;


$sth->finish;
$dbh->disconnect;
