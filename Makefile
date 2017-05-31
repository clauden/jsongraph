
YAML_PARSER = graphyaml.py
JSON_PARSER = graphjson.py


default:
	@echo "default rule"

%.png:		%.dot  
	@echo $<
	cat $< | dot -T png -o $@ 
	open $@

%.dot:		%.yaml 
	$(echo %< $@)
	python $(YAML_PARSER) > $@

%.dot:		%.json
	$(echo %< $@)
	@echo "python $(JSON_PARSER) > $@"


parse:
	$(PARSER) < $<

Xdefault:		json
	python graphjson.py
	cat out.dot |dot -Tpng -occc.png
	open ccc.png 

.PRECIOUS:	%.dot

FORCE:
