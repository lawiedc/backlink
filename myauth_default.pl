#!/usr/bin/perl

use strict;
# set up the database acess info
#
our ( $DSN, $DB_AUTH );

$DSN = 'dbi:mysql:<dbname>:<dbserver>';
$DB_AUTH = '<username>:<password>';
