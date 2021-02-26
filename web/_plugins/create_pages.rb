require "jekyll"

module FcdoPlugins
  class CreatePages < Jekyll::Generator
    safe true
    priority :normal

    def get_field_content(content, field_id, field_name)
      prefix = '<div id="' + field_id + '">'
      inner = content
      if content == '' || content == nil
        inner = '<p>' + field_name + ' (' + field_id + ') is not yet translated.</p>'
      end
      suffix = '</div>'
      return prefix + inner + suffix
    end

    def is_single_letter(character)
      return character.length == 1 && !/\A\d+\z/.match(character)
    end

    def generate(site)
      base = site.source
      platforms = {}
      site.data['countries'].each do |country, info|
        info['slug'] = country
        info['name'] = info['info']['name']
        platform = info['info']['platform']['system']
        if !platforms.has_key?(platform)
          platforms[platform] = []
        end
        platforms[platform].append(info)
      end
      site.data['countries'] = site.data['countries'].values
      site.data['countries'].each do |info|
        dir = info['slug'] + '/'
        site.pages << FcsoCountry.new(site, base, dir, info)
      end
      site.data['countries'] = site.data['countries'].sort_by {|x| x['name']}

      # Not used but left in for now.
      platforms.each do |platform, countries|
        dir = site.data['platforms'][platform]['slug']
        site.pages << FcsoPlatform.new(site, base, dir, platform, countries)
      end
    end
  end

  # A Page subclass used in the `CreatePages` class.
  class FcsoCountry < Jekyll::Page
    def initialize(site, base, dir, info)
      @site = site
      @base = base
      @dir = dir
      @name = 'index.html'

      self.process(@name)
      self.data = {}
      self.data['layout'] = 'country'
      self.data['title'] = info['name']
      self.data['info'] = info['info']
      self.data['slug'] = info['slug']
    end
  end

  # A Page subclass used in the `CreatePages` class.
  class FcsoPlatform < Jekyll::Page
    def initialize(site, base, dir, platform, countries)
      @site = site
      @base = base
      @dir = dir
      @name = 'index.html'

      self.process(@name)
      self.data = {}
      self.data['layout'] = 'platform'
      self.data['title'] = platform
      self.data['countries'] = countries
    end
  end
end
