#!/usr/bin/env ruby
#solving exercise by Guillaume Plessis of TextMe on Twitter using regular expressions
puts ARGV[0].scan(/\[from:(.*?)\] \[to:(.*?)\] \[flags:(.*?)\]/).join
