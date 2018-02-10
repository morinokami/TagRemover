#!/usr/bin/env python3

import argparse

from bs4 import BeautifulSoup


class TagRemover:
    
    def __init__(self, html_path):
        self.html_path = html_path
        with open(html_path) as f:
            self.soup = BeautifulSoup(f.read(), 'html.parser')
    
    # Remove specified classes and ids from soup.
    def remove(self, class_list=[], id_list=[]):
        def remover(identifier, finder):
            for elem in identifier:
                for tag in finder(elem):
                    tag.extract()
        
        remover(class_list, lambda e: self.soup.find_all(class_=e))
        remover(id_list, lambda e: self.soup.find_all(id=e))

    # Save soup as prettified html.
    def save(self, safe_mode=True):
        save_path = self.html_path
        if safe_mode:
            import os
            save_path = os.path.splitext(self.html_path)[0] + '_' + '.html'
        
        with open(save_path, 'w') as f:
            f.write(self.soup.prettify())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Remove specified tags from html file.')
    parser.add_argument('html_path', help='path to html file')
    parser.add_argument('--cls', nargs='*', help='classes you want to remove')
    parser.add_argument('--id', nargs='*', help='ids you want to remove')
    parser.add_argument('--safe', action='store_true', help='create another file for safety')

    args = parser.parse_args()
    
    r = TagRemover(args.html_path)
    r.remove(class_list=args.cls if args.cls else [], id_list=args.id if args.id else [])
    r.save(safe_mode=args.safe)
