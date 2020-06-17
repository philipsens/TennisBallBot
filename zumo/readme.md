# ZumoAPI
Use C-strings instead of C++'s std::str, this is because std::str likes to reallocate itself when updating its capacity.